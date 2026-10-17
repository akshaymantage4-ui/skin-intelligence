from sqlalchemy.orm import Session

from models.product import Product


def _csv(value):
    if not value:
        return set()

    if isinstance(value, list):
        return {
            str(x).strip().casefold()
            for x in value
            if str(x).strip()
        }

    return {
        x.strip().casefold()
        for x in str(value).split(",")
        if x.strip()
    }


def recommend(
    db: Session,
    skin_type: str,
    concerns: set[str],
    category: str | None,
    budget: float | None,
    goal: str | None,
    limit: int = 5
):
    query = db.query(Product).filter(
        Product.is_active == True
    )

    if category:
        query = query.filter(
            Product.category.ilike(category.strip())
        )

    if budget is not None:
        query = query.filter(
            Product.price <= budget
        )

    products = query.all()

    skin = (skin_type or "").casefold()
    goal_key = (goal or "").casefold()

    ranked = []

    for p in products:
        types = _csv(p.skin_types)
        pconcerns = _csv(p.concerns)

        score = 50
        reasons = []

        if "all" in types or skin in types:
            score += 20
            reasons.append("matches your skin type")

        overlap = concerns & pconcerns

        if overlap:
            score += min(20, 8 * len(overlap))
            reasons.append(
                "targets " + ", ".join(sorted(overlap))
            )

        if goal_key and goal_key in pconcerns:
            score += 10
            reasons.append(
                "matches your selected goal"
            )

        if budget is not None and p.price <= budget:
            reasons.append("within your budget")

        ranked.append(
            (min(score, 100), reasons, p)
        )

    ranked.sort(
        key=lambda x: (-x[0], x[2].price, x[2].name)
    )

    return [
        {
            "product": {
                "id": p.id,
                "name": p.name,
                "brand": p.brand,
                "category": p.category,
                "price": p.price,
                "key_ingredients": p.key_ingredients,
                "description": p.description
            },
            "suitability_score": score,
            "reasons": reasons or [
                "available in the selected product catalog"
            ],
        }
        for score, reasons, p in ranked[:limit]
    ]