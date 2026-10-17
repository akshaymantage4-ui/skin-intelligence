def calculate_skin_score(
    assessment,
    lifestyle,
    sleep_logs,
    routine
):

    score = 100

    # =========================
    # 1. SKIN CONDITION
    # =========================

    condition_penalty = 0

    levels = [
        assessment.acne_level,
        assessment.dryness_level,
        assessment.pigmentation_level,
        assessment.sensitivity_level
    ]

    for level in levels:

        if level:

            level = level.lower()

            if level == "medium":
                condition_penalty += 5

            elif level == "high":
                condition_penalty += 10

    condition_score = max(
        0,
        35 - condition_penalty
    )


    # =========================
    # 2. LIFESTYLE
    # =========================

    lifestyle_score = 20

    if lifestyle:

        if lifestyle.water_intake is not None:
            if lifestyle.water_intake < 2:
                lifestyle_score -= 5

        if lifestyle.sleep_hours is not None:
            if lifestyle.sleep_hours < 7:
                lifestyle_score -= 5

        if lifestyle.stress_level is not None:
            if lifestyle.stress_level >= 7:
                lifestyle_score -= 5

        if lifestyle.sun_exposure_hours is not None:
            if lifestyle.sun_exposure_hours > 3:
                lifestyle_score -= 5

    lifestyle_score = max(
        0,
        lifestyle_score
    )


    # =========================
    # 3. SLEEP
    # =========================

    sleep_score = 15

    if sleep_logs:

        valid_logs = [
            log for log in sleep_logs
            if log.sleep_duration is not None
        ]

        if valid_logs:

            average_sleep = sum(
                log.sleep_duration
                for log in valid_logs
            ) / len(valid_logs)

            if average_sleep < 7:
                sleep_score = 8

    else:

        sleep_score = 10


    # =========================
    # 4. ROUTINE CONSISTENCY
    # =========================

    routine_score = 0

    if routine:

        routine_score = 20


    # =========================
    # 5. HYDRATION
    # =========================

    hydration_score = 10

    if lifestyle:

        if lifestyle.water_intake is not None:

            if lifestyle.water_intake < 2:
                hydration_score = 5


    # =========================
    # FINAL SCORE
    # =========================

    final_score = (
        condition_score
        + lifestyle_score
        + sleep_score
        + routine_score
        + hydration_score
    )

    return {
        "skin_condition_score": condition_score,
        "lifestyle_score": lifestyle_score,
        "sleep_score": sleep_score,
        "routine_score": routine_score,
        "hydration_score": hydration_score,
        "total_score": final_score
    }