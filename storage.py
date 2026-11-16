"""JSON-backed persistence for all logged training data.

Kept as a single flat JSON file (matching the original trainer's approach)
rather than a database -- the data is small, personal, and benefits from
being human-readable/diffable. If the original tkinter version's data file
(~/.skillsusa_trainer.json) is found and this project has no data yet, its
drill/knowledge history is imported automatically so nothing is lost.
"""

import copy
import json
import os
import sys
from datetime import date, datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
DATA_FILE = DATA_DIR / "trainer_data.json"
LEGACY_FILE = Path.home() / ".skillsusa_trainer.json"

DEFAULT_DATA = {
    "drills": [],
    "knowledge_sessions": [],
    "knowledge_attempts": {},
    "mock_sessions": [],
    "packet_sessions": [],
    "settings": {
        "current_phase": 0,
        "competition_date_state": "",
        "competition_date_nationals": "",
        "notes": "",
        "track": "All",
    },
    "next_id": 1,
}


def _migrate_legacy(data):
    if not LEGACY_FILE.exists():
        return data
    try:
        with open(LEGACY_FILE, "r") as f:
            legacy = json.load(f)
    except Exception:
        return data

    for d in legacy.get("drills", []):
        data["drills"].append({
            "id": data["next_id"],
            "date": d.get("date", date.today().isoformat()),
            "source": "custom",
            "problem_id": None,
            "problem_type": d.get("problem_type", "Other"),
            "title": d.get("problem_type", "Legacy drill"),
            "time_min": d.get("time_min", 0),
            "scores": d.get("scores", {}),
            "notes": d.get("notes", ""),
            "tests_passed": None,
            "tests_total": None,
        })
        data["next_id"] += 1

    for k in legacy.get("knowledge_sessions", []):
        score_pct = k.get("score", 0)
        data["knowledge_sessions"].append({
            "id": data["next_id"],
            "date": k.get("date", date.today().isoformat()),
            "topic": k.get("topic", "Python - core syntax"),
            "num_questions": None,
            "num_correct": None,
            "score_pct": score_pct,
            "source": "legacy",
        })
        data["next_id"] += 1

    data["settings"]["current_phase"] = legacy.get("current_phase", 0)
    data["settings"]["notes"] = legacy.get("notes", "")
    return data


def load_data():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
            for key, default in DEFAULT_DATA.items():
                data.setdefault(key, copy.deepcopy(default))
            for key, default in DEFAULT_DATA["settings"].items():
                data["settings"].setdefault(key, default)
            return data
        except Exception as e:
            # Never silently discard a file we can't parse -- move it aside
            # so nothing is lost, instead of overwriting it with a blank
            # slate. This should be rare: save_data() writes atomically
            # (temp file + os.replace), so a crash mid-save can't produce
            # this; it's here for any other cause (manual edit, disk issue).
            backup = DATA_DIR / f"trainer_data.corrupt-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
            try:
                os.replace(DATA_FILE, backup)
                print(f"[storage] WARNING: {DATA_FILE} was unreadable ({e}); "
                      f"moved it to {backup} and starting a fresh data file. "
                      f"Your old data was NOT deleted -- it's in that backup file.",
                      file=sys.stderr, flush=True)
            except OSError as move_err:
                print(f"[storage] WARNING: {DATA_FILE} was unreadable ({e}) and "
                      f"could not even be backed up ({move_err}). Starting fresh "
                      f"without touching the existing file further.",
                      file=sys.stderr, flush=True)
                data = json.loads(json.dumps(DEFAULT_DATA))
                return _migrate_legacy(data)

    data = json.loads(json.dumps(DEFAULT_DATA))  # deep copy
    data = _migrate_legacy(data)
    save_data(data)
    return data


def save_data(data):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    tmp = str(DATA_FILE) + ".tmp"
    with open(tmp, "w") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp, DATA_FILE)


def _new_id(data):
    new_id = data.get("next_id", 1)
    data["next_id"] = new_id + 1
    return new_id


def add_drill(data, *, source, problem_id, problem_type, title, time_min, scores, notes,
              tests_passed=None, tests_total=None):
    entry = {
        "id": _new_id(data),
        "date": date.today().isoformat(),
        "source": source,
        "problem_id": problem_id,
        "problem_type": problem_type,
        "title": title,
        "time_min": time_min,
        "scores": scores,
        "notes": notes,
        "tests_passed": tests_passed,
        "tests_total": tests_total,
    }
    data["drills"].append(entry)
    save_data(data)
    return entry


def delete_drill(data, drill_id):
    data["drills"] = [d for d in data["drills"] if d["id"] != drill_id]
    save_data(data)


def add_knowledge_session(data, *, topic, num_questions, num_correct):
    score_pct = round(100 * num_correct / num_questions, 1) if num_questions else 0
    entry = {
        "id": _new_id(data),
        "date": date.today().isoformat(),
        "topic": topic,
        "num_questions": num_questions,
        "num_correct": num_correct,
        "score_pct": score_pct,
        "source": "quiz",
    }
    data["knowledge_sessions"].append(entry)
    save_data(data)
    return entry


def delete_knowledge_session(data, session_id):
    data["knowledge_sessions"] = [k for k in data["knowledge_sessions"] if k["id"] != session_id]
    save_data(data)


def record_knowledge_attempt(data, question_id, correct):
    stats = data["knowledge_attempts"].setdefault(question_id, {
        "seen": 0, "correct": 0, "last_date": None, "last_correct": None,
    })
    stats["seen"] += 1
    if correct:
        stats["correct"] += 1
    stats["last_date"] = date.today().isoformat()
    stats["last_correct"] = correct


def add_mock_session(data, *, problem_id, problem_title, tests_passed, tests_total,
                      quiz_topic, quiz_correct, quiz_total, rubric_scores, time_min, notes):
    entry = {
        "id": _new_id(data),
        "date": date.today().isoformat(),
        "problem_id": problem_id,
        "problem_title": problem_title,
        "tests_passed": tests_passed,
        "tests_total": tests_total,
        "quiz_topic": quiz_topic,
        "quiz_correct": quiz_correct,
        "quiz_total": quiz_total,
        "rubric_scores": rubric_scores,
        "time_min": time_min,
        "notes": notes,
    }
    data["mock_sessions"].append(entry)
    save_data(data)
    return entry


def delete_mock_session(data, session_id):
    data["mock_sessions"] = [m for m in data["mock_sessions"] if m["id"] != session_id]
    save_data(data)


def add_packet_session(data, *, problem_count, problems_submitted, problem_titles,
                        tests_passed_total, tests_total_sum, avg_rubric, total_minutes,
                        target_minutes, notes=""):
    entry = {
        "id": _new_id(data),
        "date": date.today().isoformat(),
        "problem_count": problem_count,
        "problems_submitted": problems_submitted,
        "problem_titles": problem_titles,
        "tests_passed_total": tests_passed_total,
        "tests_total_sum": tests_total_sum,
        "avg_rubric": avg_rubric,
        "total_minutes": total_minutes,
        "target_minutes": target_minutes,
        "notes": notes,
    }
    data["packet_sessions"].append(entry)
    save_data(data)
    return entry


def delete_packet_session(data, session_id):
    data["packet_sessions"] = [p for p in data["packet_sessions"] if p["id"] != session_id]
    save_data(data)


def update_settings(data, **kwargs):
    data["settings"].update(kwargs)
    save_data(data)


def reset_track_progress(data, *, question_ids, topic_names, problem_ids, category_names,
                          clear_mock_and_packet=False):
    """Wipe logged practice history belonging to one training track: quiz
    attempt stats for its questions, quiz sessions taken on its topics, and
    drill logs (bank-sourced or freeform) tied to its problems/categories.
    Settings (competition dates, phase, notes) are untouched -- this clears
    progress, not configuration."""
    data["knowledge_attempts"] = {
        qid: stats for qid, stats in data["knowledge_attempts"].items() if qid not in question_ids
    }
    data["knowledge_sessions"] = [
        k for k in data["knowledge_sessions"] if k["topic"] not in topic_names
    ]
    data["drills"] = [
        d for d in data["drills"]
        if not (
            (d.get("problem_id") and d["problem_id"] in problem_ids)
            or (not d.get("problem_id") and d.get("problem_type") in category_names)
        )
    ]
    if clear_mock_and_packet:
        data["mock_sessions"] = []
        data["packet_sessions"] = []
    save_data(data)
