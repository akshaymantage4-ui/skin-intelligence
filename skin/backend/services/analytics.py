from statistics import mean

def build_analytics(score_history, progress_logs, recommendation_history):
    progress = sorted(progress_logs, key=lambda x: x.log_date)
    scores = [float(x.skin_score) for x in progress if x.skin_score is not None]
    adherence = [float(x.routine_adherence) for x in progress if x.routine_adherence is not None]
    if not scores:
        scores = [float(x.total_score) for x in sorted(score_history, key=lambda x: x.created_at)]
    latest = scores[-1] if scores else None
    first = scores[0] if scores else None
    change = (latest - first) if latest is not None and first is not None and len(scores) > 1 else 0
    trend = "stable" if abs(change) < 2 else ("improving" if change > 0 else "declining")
    latest_adherence = adherence[-1] if adherence else None
    return {
        "latest_skin_score": latest,
        "first_skin_score": first,
        "score_change": round(change, 2),
        "trend": trend,
        "average_routine_adherence": round(mean(adherence), 2) if adherence else None,
        "latest_routine_adherence": latest_adherence,
        "progress_entries": len(progress_logs),
        "score_history_entries": len(score_history),
        "recommendation_requests": len(recommendation_history),
        "progress_timeline": [{"date": x.log_date.isoformat(), "skin_score": x.skin_score, "routine_adherence": x.routine_adherence} for x in progress],
        "notice": "Analytics summarize user-entered and system-generated records; they do not diagnose medical conditions.",
    }
