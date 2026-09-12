def generate_skincare_routine(assessment, lifestyle, analysis):
    morning_steps = [
        "Gentle cleanser",
        "Moisturizer",
        "Broad-spectrum sunscreen SPF 30+"
    ]

    evening_steps = [
        "Gentle cleanser",
        "Moisturizer"
    ]

    weekly_steps = [
        "Keep the routine simple and consistent",
        "Avoid introducing multiple new products at the same time"
    ]

    recommendations = []

    # Acne
    if assessment.acne_level:
        if assessment.acne_level.lower() in ["medium", "moderate"]:
            recommendations.append(
                "Consider a gentle acne-focused skincare product."
            )
        elif assessment.acne_level.lower() in ["high", "severe"]:
            recommendations.append(
                "Consider consulting a dermatologist for persistent or severe acne."
            )

    # Dryness
    if assessment.dryness_level:
        if assessment.dryness_level.lower() in ["medium", "moderate", "high", "severe"]:
            evening_steps.append("Use a richer moisturizer if needed")
            recommendations.append(
                "Focus on gentle cleansing and regular moisturization."
            )

    # Pigmentation
    if assessment.pigmentation_level:
        if assessment.pigmentation_level.lower() in ["medium", "moderate", "high", "severe"]:
            recommendations.append(
                "Consistent sunscreen use is important for managing pigmentation concerns."
            )

    # Sensitivity
    if assessment.sensitivity_level:
        if assessment.sensitivity_level.lower() in ["medium", "moderate", "high", "severe"]:
            recommendations.append(
                "Prefer fragrance-free and gentle skincare products."
            )
            weekly_steps.append(
                "Avoid harsh scrubs and aggressive exfoliation."
            )

    # Lifestyle
    if lifestyle:
        if lifestyle.water_intake is not None and lifestyle.water_intake < 2:
            recommendations.append(
                "Consider improving your daily water intake."
            )

        if lifestyle.sleep_hours is not None and lifestyle.sleep_hours < 7:
            recommendations.append(
                "Try to maintain a consistent sleep schedule."
            )

        if lifestyle.sun_exposure_hours is not None and lifestyle.sun_exposure_hours > 3:
            recommendations.append(
                "Use sunscreen consistently when exposed to sunlight."
            )

    return {
        "skin_type": assessment.skin_type,
        "morning_routine": morning_steps,
        "evening_routine": evening_steps,
        "weekly_routine": weekly_steps,
        "recommendations": recommendations
    }