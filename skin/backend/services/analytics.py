
from statistics import mean


def build_analytics(score_history, progress_logs, recommendation_history):
    # Sort records into chronological order.
    progress = sorted(progress_logs, key=lambda x: x.log_date)
    history = sorted(
        score_history,
        key=lambda x: x.created_at
    )

    # Use progress scores when available.
    progress_scores = [
        float(item.skin_score)
        for item in progress
        if item.skin_score is not None
    ]

    # Otherwise, use calculated skin-score history.
    history_scores = [
        float(item.total_score)
        for item in history
        if item.total_score is not None
    ]

    scores = progress_scores or history_scores

    adherence = [
        float(item.routine_adherence)
        for item in progress
        if item.routine_adherence is not None
    ]

    latest_score = scores[-1] if scores else None
    first_score = scores[0] if scores else None

    score_change = (
        latest_score - first_score
        if len(scores) > 1
        else 0
    )

    if abs(score_change) < 2:
        trend = "stable"
    elif score_change > 0:
        trend = "improving"
    else:
        trend = "declining"

    latest_adherence = adherence[-1] if adherence else None
    average_adherence = mean(adherence) if adherence else None

    progress_timeline = [
        {
            "date": item.log_date.isoformat(),
            "skin_score": item.skin_score,
            "routine_adherence": item.routine_adherence,
        }
        for item in progress
    ]

    score_history_timeline = [
        {
            "date": (
                item.created_at.isoformat()
                if item.created_at
                else None
            ),
            "total_score": float(item.total_score),
        }
        for item in history
        if item.total_score is not None
    ]

    return {
        # Existing dashboard fields
        "latest_skin_score": latest_score,
        "first_skin_score": first_score,
        "score_change": round(score_change, 2),
        "trend": trend,
        "average_routine_adherence": (
            round(average_adherence, 2)
            if average_adherence is not None
            else None
        ),
        "latest_routine_adherence": latest_adherence,
        "progress_entries": len(progress),
        "score_history_entries": len(history),
        "recommendation_requests": len(recommendation_history),
        "progress_timeline": progress_timeline,

        # Additional reporting fields
        "score_history_timeline": score_history_timeline,
        "summary": {
            "total_progress_entries": len(progress),
            "total_score_history_entries": len(history),
            "total_recommendation_requests": len(
                recommendation_history
            ),
            "scores_available": len(scores),
            "adherence_records_available": len(adherence),
        },

        "notice": (
            "Analytics summarize user-entered and system-generated "
            "records; they do not diagnose medical conditions."
        ),
    }
