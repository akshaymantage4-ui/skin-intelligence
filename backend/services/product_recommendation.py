
def normalize(value):
    """Convert value to lowercase text for matching."""
    if not value:
        return ""
    return str(value).strip().lower()


def get_product_score(product, skin_type, concerns, allergies=None):
    """Score a product based on skin type, concerns, and allergies."""
    allergies = allergies or []

    product_skin_types = [
        normalize(item)
        for item in (product.suitable_skin_types or [])
    ]

    product_concerns = [
        normalize(item)
        for item in (product.target_concerns or [])
    ]

    product_allergies = [
        normalize(item)
        for item in (product.avoids_allergies or [])
    ]

    user_skin_type = normalize(skin_type)

    user_concerns = {
        normalize(item)
        for item in (concerns or [])
    }

    user_allergies = {
        normalize(item)
        for item in allergies
    }

    # Exclude inactive products
    if not product.is_active:
        return 0

    # Exclude products that conflict with reported allergies
    if user_allergies.intersection(product_allergies):
        return 0

    score = 0

    # Skin type match
    if user_skin_type in product_skin_types:
        score += 50
    elif "all" in product_skin_types:
        score += 30

    # Concern matches
    matched_concerns = user_concerns.intersection(
        product_concerns
    )

    score += min(len(matched_concerns) * 10, 50)

    return min(score, 100)


def recommend_products(
    products,
    skin_type,
    concerns,
    allergies=None,
    budget=None
):
    """Return matching products sorted by suitability score."""
    recommendations = []

    for product in products:
        if budget is not None and product.price > budget:
            continue

        score = get_product_score(
            product=product,
            skin_type=skin_type,
            concerns=concerns,
            allergies=allergies
        )

        if score > 0:
            recommendations.append({
                "product": product,
                "suitability_score": score
            })

    recommendations.sort(
        key=lambda item: item["suitability_score"],
        reverse=True
    )

    return recommendations