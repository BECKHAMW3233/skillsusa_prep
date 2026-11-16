"""
SkillsUSA Computer Programming Competition Trainer -- web edition.
William Beckham - Spring 2027 NC State & Nationals Prep

Run with:  python app.py
Then open http://127.0.0.1:5000
"""

import os
import random
from datetime import date, datetime
from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for, jsonify, session

import storage
import quiz_engine
from runner import grade_submission
from content.meta import (
    RUBRIC_CRITERIA, PROBLEM_TYPES, DIFFICULTIES, KNOWLEDGE_TOPICS, PHASES,
    PACKET_EXCLUDED_CATEGORIES, TRACKS, TRACK_LABELS, topics_for_track, categories_for_track,
)
from content.problems import PROBLEMS, PROBLEMS_BY_ID
from content.quiz_bank import QUESTIONS, QUESTIONS_BY_TOPIC
from content import competition_info
from content.cert_info import CERT_EXAM_INFO

app = Flask(__name__)


def _load_secret_key():
    """A random key that changes every process restart would silently wipe
    every in-progress session (mid-quiz, mid-mock, mid-packet) whenever the
    dev server reloads -- including from the reloader's own false-positive
    file-change detections, which happen in practice. Persist one instead."""
    env_key = os.environ.get("SKILLSUSA_SECRET_KEY")
    if env_key:
        return env_key
    key_file = Path(__file__).parent / "data" / ".secret_key"
    key_file.parent.mkdir(parents=True, exist_ok=True)
    if key_file.exists():
        existing = key_file.read_text().strip()
        if existing:
            return existing
    new_key = os.urandom(32).hex()
    key_file.write_text(new_key)
    return new_key


app.secret_key = _load_secret_key()


# ── helpers ──────────────────────────────────────────────────────────────

def parse_scores(form):
    """Read rubric slider values from a submitted form, tolerating missing,
    non-numeric, or out-of-range input (clamped to 0-10, default 5)."""
    scores = {}
    for c in RUBRIC_CRITERIA:
        try:
            value = int(form.get(f"score_{c}", 5))
        except (TypeError, ValueError):
            value = 5
        scores[c] = max(0, min(10, value))
    return scores


def parse_time_min(form, default=0):
    try:
        value = int(form.get("time_min", default))
    except (TypeError, ValueError):
        value = default
    return max(0, value)


def _safe_int(raw):
    if raw in (None, ""):
        return None
    try:
        return int(raw)
    except (TypeError, ValueError):
        return None


def avg_rubric_scores(drills):
    scores = {}
    for c in RUBRIC_CRITERIA:
        vals = [d["scores"].get(c) for d in drills if d.get("scores") and c in d["scores"]]
        scores[c] = round(sum(vals) / len(vals), 1) if vals else None
    return scores


def days_until(iso_date):
    if not iso_date:
        return None
    try:
        target = date.fromisoformat(iso_date)
    except ValueError:
        return None
    return (target - date.today()).days


def current_track():
    return storage.load_data()["settings"].get("track", "All")


@app.context_processor
def inject_globals():
    return {
        "PROBLEM_TYPES": PROBLEM_TYPES,
        "KNOWLEDGE_TOPICS": KNOWLEDGE_TOPICS,
        "ALL_TRACKS": TRACKS,
        "TRACK_LABELS": TRACK_LABELS,
        "CURRENT_TRACK": current_track(),
    }


@app.route("/track", methods=["POST"])
def set_track():
    data = storage.load_data()
    track = request.form.get("track", "All")
    if track not in (["All"] + TRACKS):
        track = "All"
    storage.update_settings(data, track=track)
    ref = request.referrer
    if ref and ref.startswith(request.host_url):
        return redirect(ref)
    return redirect(url_for("dashboard"))


# ── dashboard ────────────────────────────────────────────────────────────

@app.route("/")
def dashboard():
    data = storage.load_data()
    drills = data["drills"]
    ksessions = data["knowledge_sessions"]
    mocks = data["mock_sessions"]
    packets = data["packet_sessions"]
    settings = data["settings"]

    rubric_avgs = avg_rubric_scores(drills)
    scored = {k: v for k, v in rubric_avgs.items() if v is not None}
    best = max(scored, key=scored.get) if scored else None
    weakest = min(scored, key=scored.get) if scored else None

    recent = list(reversed(drills[-6:]))
    recent_mocks = list(reversed(mocks[-3:]))

    return render_template(
        "dashboard.html",
        phases=PHASES,
        current_phase=settings.get("current_phase", 0),
        total_drills=len(drills),
        total_quiz_sessions=len(ksessions),
        total_mocks=len(mocks),
        total_packets=len(packets),
        rubric_avgs=rubric_avgs,
        best=best,
        weakest=weakest,
        recent=recent,
        recent_mocks=recent_mocks,
        days_state=days_until(settings.get("competition_date_state")),
        days_nationals=days_until(settings.get("competition_date_nationals")),
        settings=settings,
        cert_info=CERT_EXAM_INFO.get(settings.get("track", "All")),
    )


@app.route("/phase", methods=["POST"])
def set_phase():
    data = storage.load_data()
    try:
        idx = int(request.form["phase"])
    except (KeyError, ValueError):
        idx = 0
    idx = max(0, min(idx, len(PHASES) - 1))
    storage.update_settings(data, current_phase=idx)
    return redirect(url_for("dashboard"))


# ── settings ─────────────────────────────────────────────────────────────

@app.route("/settings", methods=["GET", "POST"])
def settings_page():
    data = storage.load_data()
    if request.method == "POST":
        storage.update_settings(
            data,
            competition_date_state=request.form.get("competition_date_state", "").strip(),
            competition_date_nationals=request.form.get("competition_date_nationals", "").strip(),
            notes=request.form.get("notes", "").strip(),
        )
        return redirect(url_for("dashboard"))
    return render_template(
        "settings.html",
        settings=data["settings"],
        tracks=TRACKS,
        track_labels=TRACK_LABELS,
        cert_exam_info=CERT_EXAM_INFO,
    )


@app.route("/settings/reset-track/<track>", methods=["POST"])
def reset_track(track):
    if track not in TRACKS:
        return redirect(url_for("settings_page"))
    data = storage.load_data()

    topic_names = set(topics_for_track(track))
    question_ids = {q["id"] for q in QUESTIONS if q["topic"] in topic_names}
    category_names = set(categories_for_track(track))
    problem_ids = {p["id"] for p in PROBLEMS if p["category"] in category_names}

    storage.reset_track_progress(
        data,
        question_ids=question_ids,
        topic_names=topic_names,
        problem_ids=problem_ids,
        category_names=category_names,
        clear_mock_and_packet=(track == "SkillsUSA"),
    )
    return redirect(url_for("settings_page"))


@app.route("/competition-format")
def competition_format():
    return render_template("competition_format.html", info=competition_info)


# ── problem bank ─────────────────────────────────────────────────────────

@app.route("/problems")
def problems_list():
    category = request.args.get("category", "")
    difficulty = request.args.get("difficulty", "")

    data = storage.load_data()
    attempted_ids = {d["problem_id"] for d in data["drills"] if d.get("problem_id")}
    track = data["settings"].get("track", "All")
    track_categories = categories_for_track(track)

    problems = [p for p in PROBLEMS if p["category"] in track_categories]
    if category:
        problems = [p for p in problems if p["category"] == category]
    if difficulty:
        problems = [p for p in problems if p["difficulty"] == difficulty]

    return render_template(
        "problems.html",
        problems=problems,
        categories=track_categories,
        difficulties=DIFFICULTIES,
        selected_category=category,
        selected_difficulty=difficulty,
        attempted_ids=attempted_ids,
    )


@app.route("/problems/<problem_id>")
def problem_detail(problem_id):
    problem = PROBLEMS_BY_ID.get(problem_id)
    if not problem:
        return redirect(url_for("problems_list"))
    return render_template("problem_detail.html", problem=problem, rubric=RUBRIC_CRITERIA)


@app.route("/problems/<problem_id>/run", methods=["POST"])
def problem_run(problem_id):
    problem = PROBLEMS_BY_ID.get(problem_id)
    if not problem:
        return jsonify({"error": "unknown problem"}), 404
    code = request.json.get("code", "") if request.is_json else request.form.get("code", "")
    result = grade_submission(code, problem["test_cases"])
    return jsonify(result)


@app.route("/problems/<problem_id>/log", methods=["POST"])
def problem_log(problem_id):
    problem = PROBLEMS_BY_ID.get(problem_id)
    if not problem:
        return redirect(url_for("problems_list"))

    data = storage.load_data()
    scores = parse_scores(request.form)
    time_min = parse_time_min(request.form)
    tests_passed = request.form.get("tests_passed")
    tests_total = request.form.get("tests_total")

    storage.add_drill(
        data,
        source="bank",
        problem_id=problem_id,
        problem_type=problem["category"],
        title=problem["title"],
        time_min=time_min,
        scores=scores,
        notes=request.form.get("notes", "").strip(),
        tests_passed=_safe_int(tests_passed),
        tests_total=_safe_int(tests_total),
    )
    return redirect(url_for("problem_detail", problem_id=problem_id, logged=1))


# ── freeform drill log (practice done outside the bank) ────────────────────

@app.route("/drill", methods=["GET", "POST"])
def drill_log():
    if request.method == "POST":
        data = storage.load_data()
        scores = parse_scores(request.form)
        time_min = parse_time_min(request.form)
        storage.add_drill(
            data,
            source="custom",
            problem_id=None,
            problem_type=request.form.get("problem_type", "Other"),
            title=request.form.get("problem_type", "Other"),
            time_min=time_min,
            scores=scores,
            notes=request.form.get("notes", "").strip(),
        )
        return redirect(url_for("drill_log", logged=1))
    track = storage.load_data()["settings"].get("track", "All")
    return render_template("drill_log.html", rubric=RUBRIC_CRITERIA, problem_types=categories_for_track(track))


# ── timer ────────────────────────────────────────────────────────────────

@app.route("/timer")
def timer_page():
    return render_template("timer.html")


# ── knowledge quiz ───────────────────────────────────────────────────────

@app.route("/quiz")
def quiz_setup():
    data = storage.load_data()
    track = data["settings"].get("track", "All")
    track_topics = topics_for_track(track)
    coverage = []
    attempts = data.get("knowledge_attempts", {})
    for topic in track_topics:
        qs = QUESTIONS_BY_TOPIC.get(topic, [])
        seen = sum(1 for q in qs if q["id"] in attempts)
        wrong = sum(
            1 for q in qs
            if q["id"] in attempts and attempts[q["id"]]["seen"] > attempts[q["id"]]["correct"]
        )
        coverage.append({
            "topic": topic,
            "total_questions": len(qs),
            "seen": seen,
            "weak": wrong,
        })
    return render_template("quiz_setup.html", topics=track_topics, coverage=coverage)


@app.route("/quiz/start", methods=["POST"])
def quiz_start():
    data = storage.load_data()
    track = data["settings"].get("track", "All")
    topic = request.form.get("topic") or None
    try:
        count = int(request.form.get("count", 10))
    except ValueError:
        count = 10
    count = max(3, min(count, 40))

    mixed_pool = None
    if (not topic or topic == "Mixed Review") and track != "All":
        track_topics = set(topics_for_track(track))
        mixed_pool = [q for q in QUESTIONS if q["topic"] in track_topics]

    questions = quiz_engine.select_questions(data, topic, count, mixed_pool=mixed_pool)
    session["quiz_question_ids"] = [q["id"] for q in questions]
    session["quiz_topic"] = topic or "Mixed Review"
    return redirect(url_for("quiz_run"))


@app.route("/quiz/run")
def quiz_run():
    ids = session.get("quiz_question_ids")
    if not ids:
        return redirect(url_for("quiz_setup"))
    questions = quiz_engine.get_questions(ids)
    return render_template("quiz_run.html", questions=questions, topic=session.get("quiz_topic"))


@app.route("/quiz/submit", methods=["POST"])
def quiz_submit():
    ids = session.get("quiz_question_ids")
    if not ids:
        return redirect(url_for("quiz_setup"))

    answers = {}
    for qid in ids:
        answers[qid] = _safe_int(request.form.get(f"answer_{qid}"))

    graded = quiz_engine.grade_answers(ids, answers)

    data = storage.load_data()
    for r in graded["results"]:
        storage.record_knowledge_attempt(data, r["id"], r["correct"])
    storage.add_knowledge_session(
        data,
        topic=session.get("quiz_topic", "Mixed Review"),
        num_questions=graded["total"],
        num_correct=graded["correct"],
    )

    session["quiz_result"] = graded
    session.pop("quiz_question_ids", None)
    return redirect(url_for("quiz_result"))


@app.route("/quiz/result")
def quiz_result():
    graded = session.get("quiz_result")
    if not graded:
        return redirect(url_for("quiz_setup"))
    return render_template("quiz_result.html", graded=graded, topic=session.get("quiz_topic"))


# ── mock competition (timed knowledge + coding combo) ───────────────────
#
# Mock Competition simulates the SkillsUSA contest format specifically (a
# timed coding problem plus a knowledge test, scored together), so its
# problem/topic pools are always drawn from the SkillsUSA track regardless
# of whichever training track is currently selected elsewhere in the app.

def _skillsusa_problems():
    skillsusa_categories = set(categories_for_track("SkillsUSA"))
    return [p for p in PROBLEMS if p["category"] in skillsusa_categories]


@app.route("/mock")
def mock_setup():
    return render_template(
        "mock_setup.html",
        problems=_skillsusa_problems(),
        topics=["Mixed Review"] + topics_for_track("SkillsUSA"),
    )


@app.route("/mock/start", methods=["POST"])
def mock_start():
    data = storage.load_data()
    problem_id = request.form.get("problem_id")
    if problem_id not in {p["id"] for p in _skillsusa_problems()}:
        return redirect(url_for("mock_setup"))
    topic = request.form.get("topic") or None
    try:
        count = int(request.form.get("count", 8))
    except ValueError:
        count = 8
    count = max(3, min(count, 25))

    skillsusa_topics = set(topics_for_track("SkillsUSA"))
    mixed_pool = [q for q in QUESTIONS if q["topic"] in skillsusa_topics]
    questions = quiz_engine.select_questions(data, topic, count, mixed_pool=mixed_pool)
    session["mock_problem_id"] = problem_id
    session["mock_question_ids"] = [q["id"] for q in questions]
    session["mock_topic"] = topic or "Mixed Review"
    session["mock_start"] = datetime.now().isoformat()
    return redirect(url_for("mock_run"))


@app.route("/mock/run")
def mock_run():
    problem_id = session.get("mock_problem_id")
    ids = session.get("mock_question_ids")
    if not problem_id or ids is None:
        return redirect(url_for("mock_setup"))
    problem = PROBLEMS_BY_ID[problem_id]
    questions = quiz_engine.get_questions(ids)
    total_minutes = problem["time_limit_min"] + max(1, len(questions) // 2)
    return render_template(
        "mock_run.html",
        problem=problem,
        questions=questions,
        rubric=RUBRIC_CRITERIA,
        total_minutes=total_minutes,
    )


@app.route("/mock/submit", methods=["POST"])
def mock_submit():
    problem_id = session.get("mock_problem_id")
    ids = session.get("mock_question_ids")
    if not problem_id or ids is None:
        return redirect(url_for("mock_setup"))
    problem = PROBLEMS_BY_ID[problem_id]

    answers = {}
    for qid in ids:
        answers[qid] = _safe_int(request.form.get(f"answer_{qid}"))
    graded = quiz_engine.grade_answers(ids, answers)

    code = request.form.get("code", "")
    test_result = grade_submission(code, problem["test_cases"])

    scores = parse_scores(request.form)
    start_iso = session.get("mock_start")
    time_min = 0
    if start_iso:
        try:
            elapsed = datetime.now() - datetime.fromisoformat(start_iso)
            time_min = round(elapsed.total_seconds() / 60)
        except ValueError:
            pass

    data = storage.load_data()
    for r in graded["results"]:
        storage.record_knowledge_attempt(data, r["id"], r["correct"])
    storage.add_knowledge_session(
        data,
        topic=session.get("mock_topic", "Mixed Review"),
        num_questions=graded["total"],
        num_correct=graded["correct"],
    )
    storage.add_mock_session(
        data,
        problem_id=problem_id,
        problem_title=problem["title"],
        tests_passed=test_result["passed"],
        tests_total=test_result["total"],
        quiz_topic=session.get("mock_topic", "Mixed Review"),
        quiz_correct=graded["correct"],
        quiz_total=graded["total"],
        rubric_scores=scores,
        time_min=time_min,
        notes=request.form.get("notes", "").strip(),
    )

    session["mock_result"] = {"quiz": graded, "tests": test_result, "problem_title": problem["title"]}
    for key in ("mock_problem_id", "mock_question_ids", "mock_topic", "mock_start"):
        session.pop(key, None)
    return redirect(url_for("mock_result"))


@app.route("/mock/result")
def mock_result():
    result = session.get("mock_result")
    if not result:
        return redirect(url_for("mock_setup"))
    return render_template("mock_result.html", result=result)


# ── packet mode (real contest format: 3-4 programs, one shared clock) ────
#
# Mirrors the actual national packet process documented in
# content/competition_info.py: finish a program, "hand it in" (submitted
# with its results recorded against the shared clock), move to the next.
# The clock never pauses and keeps running across page loads/navigation --
# elapsed time is always recomputed from the wall-clock session["packet_start"]
# timestamp, not from client-side JS state alone.

def _packetable_problems():
    return [p for p in PROBLEMS if p["category"] not in PACKET_EXCLUDED_CATEGORIES]


def _generate_packet(count):
    """Draw `count` distinct problems, preferring one per category (like a
    real packet drawing from different program types) before repeating."""
    pool = _packetable_problems()
    by_category = {}
    for p in pool:
        by_category.setdefault(p["category"], []).append(p)
    categories = list(by_category.keys())
    random.shuffle(categories)

    chosen = []
    chosen_ids = set()
    for cat in categories:
        if len(chosen) >= count:
            break
        candidate = random.choice(by_category[cat])
        chosen.append(candidate)
        chosen_ids.add(candidate["id"])

    remaining = [p for p in pool if p["id"] not in chosen_ids]
    random.shuffle(remaining)
    while len(chosen) < count and remaining:
        candidate = remaining.pop()
        chosen.append(candidate)
        chosen_ids.add(candidate["id"])

    return [p["id"] for p in chosen]


def _packet_elapsed_minutes():
    start_iso = session.get("packet_start")
    if not start_iso:
        return 0
    try:
        elapsed = datetime.now() - datetime.fromisoformat(start_iso)
    except ValueError:
        return 0
    return max(0, round(elapsed.total_seconds() / 60))


def _packet_elapsed_ms():
    start_iso = session.get("packet_start")
    if not start_iso:
        return 0
    try:
        elapsed = datetime.now() - datetime.fromisoformat(start_iso)
    except ValueError:
        return 0
    return max(0, round(elapsed.total_seconds() * 1000))


@app.route("/packet")
def packet_setup():
    return render_template("packet_setup.html", problems=_packetable_problems())


@app.route("/packet/start", methods=["POST"])
def packet_start():
    try:
        count = int(request.form.get("count", 4))
    except (TypeError, ValueError):
        count = 4
    count = max(3, min(count, 4))

    if request.form.get("mode") == "manual":
        pool_ids = {p["id"] for p in _packetable_problems()}
        ids = [i for i in request.form.getlist("problem_id") if i in pool_ids][:4]
        if len(ids) < 3:
            return redirect(url_for("packet_setup"))
    else:
        ids = _generate_packet(count)

    problems = [PROBLEMS_BY_ID[i] for i in ids]
    session["packet_ids"] = ids
    session["packet_start"] = datetime.now().isoformat()
    session["packet_target"] = sum(p["time_limit_min"] for p in problems)
    session["packet_handins"] = {}
    return redirect(url_for("packet_run"))


@app.route("/packet/run")
def packet_run():
    ids = session.get("packet_ids")
    if not ids:
        return redirect(url_for("packet_setup"))
    problems = [PROBLEMS_BY_ID[i] for i in ids if i in PROBLEMS_BY_ID]
    return render_template(
        "packet_run.html",
        problems=problems,
        handins=session.get("packet_handins", {}),
        target_minutes=session.get("packet_target", 0),
        elapsed_ms=_packet_elapsed_ms(),
    )


@app.route("/packet/problem/<problem_id>")
def packet_problem(problem_id):
    ids = session.get("packet_ids")
    if not ids or problem_id not in ids:
        return redirect(url_for("packet_setup"))
    problem = PROBLEMS_BY_ID.get(problem_id)
    if not problem:
        return redirect(url_for("packet_run"))
    return render_template(
        "packet_problem.html",
        problem=problem,
        rubric=RUBRIC_CRITERIA,
        handin=session.get("packet_handins", {}).get(problem_id),
        target_minutes=session.get("packet_target", 0),
        elapsed_ms=_packet_elapsed_ms(),
    )


@app.route("/packet/problem/<problem_id>/run", methods=["POST"])
def packet_problem_run(problem_id):
    problem = PROBLEMS_BY_ID.get(problem_id)
    if not problem:
        return jsonify({"error": "unknown problem"}), 404
    code = request.json.get("code", "") if request.is_json else request.form.get("code", "")
    result = grade_submission(code, problem["test_cases"])
    return jsonify(result)


@app.route("/packet/problem/<problem_id>/submit", methods=["POST"])
def packet_problem_submit(problem_id):
    ids = session.get("packet_ids")
    if not ids or problem_id not in ids:
        return redirect(url_for("packet_setup"))
    if problem_id not in PROBLEMS_BY_ID:
        return redirect(url_for("packet_run"))

    handins = session.get("packet_handins", {})
    handins[problem_id] = {
        "tests_passed": _safe_int(request.form.get("tests_passed")),
        "tests_total": _safe_int(request.form.get("tests_total")),
        "scores": parse_scores(request.form),
        "handin_minute": _packet_elapsed_minutes(),
    }
    session["packet_handins"] = handins
    return redirect(url_for("packet_run"))


@app.route("/packet/finish", methods=["POST"])
def packet_finish():
    ids = session.get("packet_ids")
    if not ids:
        return redirect(url_for("packet_setup"))
    problems = [PROBLEMS_BY_ID[i] for i in ids if i in PROBLEMS_BY_ID]
    handins = session.get("packet_handins", {})
    total_minutes = _packet_elapsed_minutes()
    target_minutes = session.get("packet_target", 0)

    results = []
    tests_passed_total = 0
    tests_total_sum = 0
    rubric_avgs = []
    for p in problems:
        h = handins.get(p["id"])
        if h:
            tests_passed_total += h.get("tests_passed") or 0
            tests_total_sum += h.get("tests_total") or 0
            scores = h.get("scores") or {}
            if scores:
                rubric_avgs.append(sum(scores.values()) / len(scores))
        results.append({
            "id": p["id"],
            "title": p["title"],
            "category": p["category"],
            "difficulty": p["difficulty"],
            "submitted": h is not None,
            "tests_passed": h.get("tests_passed") if h else None,
            "tests_total": h.get("tests_total") if h else None,
            "handin_minute": h.get("handin_minute") if h else None,
        })

    submitted_count = sum(1 for r in results if r["submitted"])
    avg_rubric = round(sum(rubric_avgs) / len(rubric_avgs), 1) if rubric_avgs else None

    data = storage.load_data()
    storage.add_packet_session(
        data,
        problem_count=len(problems),
        problems_submitted=submitted_count,
        problem_titles=[p["title"] for p in problems],
        tests_passed_total=tests_passed_total,
        tests_total_sum=tests_total_sum,
        avg_rubric=avg_rubric,
        total_minutes=total_minutes,
        target_minutes=target_minutes,
    )

    session["packet_result"] = {
        "results": results,
        "submitted_count": submitted_count,
        "total_count": len(problems),
        "total_minutes": total_minutes,
        "target_minutes": target_minutes,
        "tests_passed_total": tests_passed_total,
        "tests_total_sum": tests_total_sum,
        "avg_rubric": avg_rubric,
    }
    for key in ("packet_ids", "packet_start", "packet_target", "packet_handins"):
        session.pop(key, None)
    return redirect(url_for("packet_result"))


@app.route("/packet/result")
def packet_result():
    result = session.get("packet_result")
    if not result:
        return redirect(url_for("packet_setup"))
    return render_template("packet_result.html", result=result)


# ── history ──────────────────────────────────────────────────────────────

@app.route("/history")
def history():
    data = storage.load_data()
    drills = list(reversed(data["drills"]))
    ksessions = list(reversed(data["knowledge_sessions"]))
    mocks = list(reversed(data["mock_sessions"]))
    packets = list(reversed(data["packet_sessions"]))
    return render_template("history.html", drills=drills, ksessions=ksessions, mocks=mocks, packets=packets)


@app.route("/history/delete/drill/<int:item_id>", methods=["POST"])
def delete_drill(item_id):
    data = storage.load_data()
    storage.delete_drill(data, item_id)
    return redirect(url_for("history"))


@app.route("/history/delete/knowledge/<int:item_id>", methods=["POST"])
def delete_knowledge(item_id):
    data = storage.load_data()
    storage.delete_knowledge_session(data, item_id)
    return redirect(url_for("history"))


@app.route("/history/delete/mock/<int:item_id>", methods=["POST"])
def delete_mock(item_id):
    data = storage.load_data()
    storage.delete_mock_session(data, item_id)
    return redirect(url_for("history"))


@app.route("/history/delete/packet/<int:item_id>", methods=["POST"])
def delete_packet(item_id):
    data = storage.load_data()
    storage.delete_packet_session(data, item_id)
    return redirect(url_for("history"))


# ── progress ─────────────────────────────────────────────────────────────

@app.route("/progress")
def progress():
    data = storage.load_data()
    drills = data["drills"]
    ksessions = data["knowledge_sessions"]

    rubric_series = {c: [] for c in RUBRIC_CRITERIA}
    labels = []
    for d in drills:
        labels.append(d["date"])
        for c in RUBRIC_CRITERIA:
            rubric_series[c].append(d.get("scores", {}).get(c))

    time_series = [d.get("time_min", 0) for d in drills]

    quiz_labels = [k["date"] for k in ksessions]
    quiz_scores = [k["score_pct"] for k in ksessions]

    coverage = []
    attempts = data.get("knowledge_attempts", {})
    track = data["settings"].get("track", "All")
    for topic in topics_for_track(track):
        qs = QUESTIONS_BY_TOPIC.get(topic, [])
        seen = [attempts[q["id"]] for q in qs if q["id"] in attempts]
        if seen:
            total_seen = sum(s["seen"] for s in seen)
            total_correct = sum(s["correct"] for s in seen)
            pct = round(100 * total_correct / total_seen, 1) if total_seen else 0
        else:
            pct = None
        coverage.append({"topic": topic, "pct": pct, "questions_seen": len(seen), "questions_total": len(qs)})

    return render_template(
        "progress.html",
        has_drills=len(drills) >= 2,
        has_quiz=len(ksessions) >= 1,
        labels=labels,
        rubric_series=rubric_series,
        rubric_criteria=RUBRIC_CRITERIA,
        time_series=time_series,
        quiz_labels=quiz_labels,
        quiz_scores=quiz_scores,
        coverage=coverage,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
