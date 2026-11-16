"""Question selection (lightweight spaced repetition) and grading."""

import random
from datetime import date

from content.quiz_bank import QUESTIONS, QUESTIONS_BY_TOPIC, QUESTIONS_BY_ID


def _weight_for(question, attempts):
    stats = attempts.get(question["id"])
    if not stats or stats.get("seen", 0) == 0:
        return 4.0  # never seen -- prioritize new material

    seen = stats["seen"]
    correct = stats.get("correct", 0)
    wrong_rate = 1 - (correct / seen)

    days_stale = 0
    last_date = stats.get("last_date")
    if last_date:
        try:
            days_stale = (date.today() - date.fromisoformat(last_date)).days
        except ValueError:
            days_stale = 0

    weight = 0.6 + wrong_rate * 3.0 + min(days_stale, 30) * 0.04
    return max(weight, 0.05)


def _weighted_sample(items, weights, k):
    """Weighted sampling without replacement (Efraimidis-Spirakis)."""
    keyed = []
    for item, w in zip(items, weights):
        w = max(w, 1e-6)
        u = random.random()
        key = u ** (1.0 / w)
        keyed.append((key, item))
    keyed.sort(key=lambda pair: pair[0], reverse=True)
    return [item for _, item in keyed[:k]]


def select_questions(data, topic, count, mixed_pool=None):
    """topic=None (or 'Mixed Review') pulls from every topic (or from
    `mixed_pool`, when the caller wants Mixed Review narrowed to a training
    track's topics), weighted toward weak/never-seen questions."""
    if not topic or topic == "Mixed Review":
        pool = mixed_pool if mixed_pool is not None else QUESTIONS
    else:
        pool = QUESTIONS_BY_TOPIC.get(topic, [])
    if not pool:
        return []
    attempts = data.get("knowledge_attempts", {})
    weights = [_weight_for(q, attempts) for q in pool]
    count = min(count, len(pool))
    return _weighted_sample(pool, weights, count)


def get_questions(ids):
    return [QUESTIONS_BY_ID[i] for i in ids if i in QUESTIONS_BY_ID]


def grade_answers(question_ids, submitted_answers):
    """submitted_answers: dict of question_id -> chosen index (int or None).
    Returns per-question results and an overall score."""
    results = []
    correct_count = 0
    for qid in question_ids:
        q = QUESTIONS_BY_ID.get(qid)
        if not q:
            continue
        chosen = submitted_answers.get(qid)
        is_correct = chosen is not None and int(chosen) == q["answer"]
        if is_correct:
            correct_count += 1
        results.append({
            "id": qid,
            "question": q["question"],
            "choices": q["choices"],
            "answer": q["answer"],
            "chosen": chosen,
            "correct": is_correct,
            "explanation": q["explanation"],
        })
    return {
        "results": results,
        "correct": correct_count,
        "total": len(results),
        "score_pct": round(100 * correct_count / len(results), 1) if results else 0,
    }
