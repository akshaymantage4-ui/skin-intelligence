"""Rules used to turn a questionnaire into clear, non-diagnostic skin insights."""

SEVERITY = {"low": 1, "medium": 2, "moderate": 2, "high": 3, "severe": 3}
CONCERN_LABELS = {"acne_level": "Acne", "dryness_level": "Dryness", "pigmentation_level": "Pigmentation", "sensitivity_level": "Sensitivity"}


def _level(value):
    return SEVERITY.get((value or "").strip().lower(), 0)


def analyze_skin_assessment(assessment, lifestyle, sleep_logs, environment=None):
    """Return explainable assessment results, rather than a medical diagnosis."""
    priorities, risk_factors = [], []
    for field, label in CONCERN_LABELS.items():
        severity = _level(getattr(assessment, field, None))
        if severity:
            level = (getattr(assessment, field) or "").strip().title()
            priorities.append({"concern": label, "severity": level, "priority": severity})
            if severity >= 2:
                risk_factors.append(f"{level} {label.lower()} needs a gentle, consistent routine.")
    priorities.sort(key=lambda concern: concern["priority"], reverse=True)
    skin_concerns = [f"{item['severity']} {item['concern'].lower()} concern" for item in priorities] or ["No questionnaire concerns were selected."]

    lifestyle_analysis = []
    if lifestyle:
        if lifestyle.water_intake is not None and lifestyle.water_intake < 2:
            lifestyle_analysis.append("Daily water intake is below 2 litres.")
            risk_factors.append("Low hydration can make dryness feel more noticeable.")
        if lifestyle.sleep_hours is not None and lifestyle.sleep_hours < 7:
            lifestyle_analysis.append("Reported sleep duration is below 7 hours.")
            risk_factors.append("Short sleep can affect skin recovery.")
        if lifestyle.stress_level is not None and lifestyle.stress_level >= 3:
            lifestyle_analysis.append("High stress was reported.")
            risk_factors.append("Stress may contribute to skin flare-ups.")
        if lifestyle.sun_exposure_hours is not None and lifestyle.sun_exposure_hours > 3:
            lifestyle_analysis.append("Daily sun exposure is above 3 hours.")
            risk_factors.append("Higher sun exposure increases the importance of sun protection.")

    durations = [log.sleep_duration for log in sleep_logs if log.sleep_duration is not None]
    sleep_analysis = [f"Average logged sleep: {sum(durations) / len(durations):.1f} hours per night."] if durations else ["No sleep logs yet; add them to improve future insights."]
    if durations and sum(durations) / len(durations) < 7:
        risk_factors.append("Recent sleep logs are below the 7-hour target.")

    environment_analysis = []
    if environment:
        if environment.uv_index is not None and environment.uv_index >= 6:
            environment_analysis.append("UV exposure is high; use broad-spectrum SPF 30+ daily.")
        if environment.pollution_level is not None and environment.pollution_level > 100:
            environment_analysis.append("Higher pollution can make gentle evening cleansing useful.")

    return {"skin_type": assessment.skin_type, "skin_concerns": skin_concerns, "concern_priorities": priorities, "risk_factors": risk_factors, "lifestyle_analysis": lifestyle_analysis or ["No lifestyle risk factors were identified."], "sleep_analysis": sleep_analysis, "environment_analysis": environment_analysis, "additional_concerns": assessment.additional_concerns, "disclaimer": "This is skincare guidance, not a medical diagnosis. Seek a dermatologist for persistent or severe concerns."}
