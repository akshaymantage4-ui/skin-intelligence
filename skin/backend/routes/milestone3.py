import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from dependencies.auth import get_current_user
from models.skin_assessment import SkinAssessment
from models.skin_profile import SkinProfile
from models.lifestyle_profile import LifestyleProfile
from models.ingredient_analysis import IngredientAnalysisHistory
from models.product import Product
from models.product_recommendation import ProductRecommendationHistory
from models.progress_log import ProgressLog
from models.skin_score_history import SkinScoreHistory
from schemas.milestone3 import IngredientAnalyzeRequest, ProductRecommendationRequest, ProgressLogCreate, ProgressLogResponse, ProductCompareRequest
from services.ingredient_intelligence import analyze
from services.product_recommendation import recommend
from services.analytics import build_analytics
from models.sleep_log import SleepLog
from models.skincare_routine import SkincareRoutine
from services.skin_score import calculate_skin_score
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def _user_id(current_user):
    return current_user.id if hasattr(current_user, "id") else current_user["id"]

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

def _concerns(assessment, profile):
    result = set()
    mapping = [("acne_level", "acne"), ("dryness_level", "dryness"), ("pigmentation_level", "pigmentation"), ("sensitivity_level", "sensitivity")]
    for field, label in mapping:
        value = getattr(assessment, field, None) if assessment else None
        if value and str(value).casefold() not in {"none", "low", "mild"}:
            result.add(label)
    if profile:
        for label in ["acne", "dryness", "pigmentation", "sensitivity"]:
            if getattr(profile, label, False): result.add(label)
    if assessment and assessment.additional_concerns:
        result.update(x.strip().casefold() for x in assessment.additional_concerns.split(",") if x.strip())
    return result

@router.post("/ingredients/analyze")
def analyze_ingredients(request: IngredientAnalyzeRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    result = analyze(request.ingredients)
    uid = _user_id(current_user)
    for item in result["ingredients"]:
        db.add(IngredientAnalysisHistory(user_id=uid, ingredient_name=item["display_name"], result_json=json.dumps(item)))
    db.commit()
    return result

@router.get("/ingredients/history")
def ingredient_history(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    uid = _user_id(current_user)
    rows = db.query(IngredientAnalysisHistory).filter(IngredientAnalysisHistory.user_id == uid).order_by(IngredientAnalysisHistory.created_at.desc()).limit(50).all()
    return rows

@router.post("/ingredients/suitability")
def ingredient_suitability(request: IngredientAnalyzeRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    uid = _user_id(current_user)
    assessment = db.query(SkinAssessment).filter(SkinAssessment.user_id == uid).first()
    profile = db.query(SkinProfile).filter(SkinProfile.user_id == uid).first()
    if not assessment and not profile:
        raise HTTPException(status_code=404, detail="Complete your skin profile or assessment first")
    result = analyze(request.ingredients)
    concerns = _concerns(assessment, profile)
    skin_type = (assessment.skin_type if assessment else profile.skin_type)
    for item in result["ingredients"]:
        flags = item["reference_flags"]
        item["user_skin_type"] = skin_type
        item["user_concerns"] = sorted(concerns)
        item["reference_notes"] = []
        if flags["fragrance"] or flags["eu_allergen"]: item["reference_notes"].append("Contains a fragrance/allergen reference flag; review the full ingredient list if you have known sensitivities.")
        if flags["pregnancy_caution"]: item["reference_notes"].append("Reference dataset marks pregnancy caution; discuss use with a qualified clinician if relevant.")
        if flags["fungal_acne_trigger"]: item["reference_notes"].append("Reference dataset marks a fungal-acne-trigger flag.")
    return {**result, "skin_profile": {"skin_type": skin_type, "concerns": sorted(concerns)}}

@router.post("/products/recommendations")
def product_recommendations(request: ProductRecommendationRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    uid = _user_id(current_user)
    assessment = db.query(SkinAssessment).filter(SkinAssessment.user_id == uid).first()
    profile = db.query(SkinProfile).filter(SkinProfile.user_id == uid).first()
    if not assessment and not profile:
        raise HTTPException(status_code=404, detail="Complete your skin profile or assessment first")
    skin_type = assessment.skin_type if assessment else profile.skin_type
    results = recommend(db, skin_type, _concerns(assessment, profile), request.category, request.budget, request.goal, request.limit)
    payload = {"skin_type": skin_type, "request": request.model_dump(), "recommendations": results, "notice": "Catalog-based recommendations for demonstration; not medical advice."}
    db.add(ProductRecommendationHistory(user_id=uid, request_json=json.dumps(request.model_dump()), result_json=json.dumps(payload)))
    db.commit()
    return payload


@router.post("/products/compare")
def compare_products(request: ProductCompareRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    rows = db.query(Product).filter(Product.id.in_(request.product_ids), Product.is_active == True).all()
    if len(rows) < 2:
        raise HTTPException(status_code=404, detail="Select at least two valid products to compare")
    return [{"id": p.id, "name": p.name, "brand": p.brand, "category": p.category, "price": p.price, "skin_types": p.skin_types, "concerns": p.concerns, "key_ingredients": p.key_ingredients, "description": p.description} for p in rows]

@router.get("/products/{product_id}/alternatives")
def product_alternatives(product_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    source = db.query(Product).filter(Product.id == product_id, Product.is_active == True).first()
    if not source:
        raise HTTPException(status_code=404, detail="Product not found")
    source_concerns = _csv(source.concerns)
    candidates = db.query(Product).filter(Product.category == source.category, Product.id != source.id, Product.is_active == True).all()
    ranked = sorted(candidates, key=lambda p: (-len(source_concerns & _csv(p.concerns)), abs(p.price - source.price), p.name))
    return ranked[:5]

@router.get("/products")
def products(category: str | None = None, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    q = db.query(Product).filter(Product.is_active == True)
    if category: q = q.filter(Product.category.ilike(category))
    return q.order_by(Product.category, Product.price).all()

@router.get("/products/recommendation-history")
def recommendation_history(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    uid = _user_id(current_user)
    return db.query(ProductRecommendationHistory).filter(ProductRecommendationHistory.user_id == uid).order_by(ProductRecommendationHistory.created_at.desc()).limit(20).all()

@router.post("/progress", response_model=ProgressLogResponse)
def create_progress(item: ProgressLogCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    uid = _user_id(current_user)
    row = ProgressLog(user_id=uid, **item.model_dump())
    db.add(row); db.commit(); db.refresh(row)
    return row

@router.get("/progress", response_model=list[ProgressLogResponse])
def get_progress(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    uid = _user_id(current_user)
    return db.query(ProgressLog).filter(ProgressLog.user_id == uid).order_by(ProgressLog.log_date.desc()).all()

@router.delete("/progress/{progress_id}")
def delete_progress(progress_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    uid = _user_id(current_user)
    row = db.query(ProgressLog).filter(ProgressLog.id == progress_id, ProgressLog.user_id == uid).first()
    if not row: raise HTTPException(status_code=404, detail="Progress entry not found")
    db.delete(row); db.commit(); return {"message": "Progress entry deleted"}


@router.get("/progress/comparison")
def progress_comparison(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    uid = _user_id(current_user)
    rows = db.query(ProgressLog).filter(ProgressLog.user_id == uid).order_by(ProgressLog.log_date.asc()).all()
    if len(rows) < 2:
        return {"available": False, "message": "Add at least two progress entries for a before/after comparison."}
    first, latest = rows[0], rows[-1]
    return {"available": True, "before": first, "after": latest, "skin_score_change": (latest.skin_score - first.skin_score) if latest.skin_score is not None and first.skin_score is not None else None, "adherence_change": (latest.routine_adherence - first.routine_adherence) if latest.routine_adherence is not None and first.routine_adherence is not None else None}

@router.get("/analytics/dashboard")
def analytics_dashboard(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    uid = _user_id(current_user)
    return build_analytics(
        db.query(SkinScoreHistory).filter(SkinScoreHistory.user_id == uid).order_by(SkinScoreHistory.created_at).all(),
        db.query(ProgressLog).filter(ProgressLog.user_id == uid).order_by(ProgressLog.log_date).all(),
        db.query(ProductRecommendationHistory).filter(ProductRecommendationHistory.user_id == uid).all(),
    )
@router.get("/skin-score")
def get_skin_score(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    uid = _user_id(current_user)

    # 1. Get the user's skin assessment
    assessment = (
        db.query(SkinAssessment)
        .filter(SkinAssessment.user_id == uid)
        .first()
    )

    if not assessment:
        raise HTTPException(
            status_code=404,
            detail="Complete your skin assessment first"
        )

    # 2. Get lifestyle profile
    lifestyle = (
        db.query(LifestyleProfile)
        .filter(LifestyleProfile.user_id == uid)
        .first()
    )

    # 3. Get the user's sleep logs
    sleep_logs = (
        db.query(SleepLog)
        .filter(SleepLog.user_id == uid)
        .order_by(SleepLog.sleep_date.desc())
        .limit(7)
        .all()
    )

    # 4. Get skincare routine
    routine = (
        db.query(SkincareRoutine)
        .filter(SkincareRoutine.user_id == uid)
        .first()
    )

    # 5. Calculate skin score
    result = calculate_skin_score(
        assessment,
        lifestyle,
        sleep_logs,
        routine
    )

    # 6. Save score history
    history = SkinScoreHistory(
        user_id=uid,
        total_score=result["total_score"],
        skin_condition_score=result["skin_condition_score"],
        lifestyle_score=result["lifestyle_score"],
        sleep_score=result["sleep_score"],
        routine_score=result["routine_score"],
        hydration_score=result["hydration_score"]
    )

    db.add(history)
    db.commit()
    db.refresh(history)

    # 7. Return result
    return {
        **result,
        "history_id": history.id,
        "created_at": history.created_at,
        "notice": (
            "This is a demonstration score based on recorded data, "
            "not a medical assessment."
        )
    }


@router.get("/skincare-routine")
def get_skincare_routine(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    uid = _user_id(current_user)

    routine = db.query(SkincareRoutine).filter(
        SkincareRoutine.user_id == uid
    ).first()

    if not routine:
        raise HTTPException(
            status_code=404,
            detail="Skincare routine not found"
        )

    return routine


# @router.get("/progress")
# def get_progress(
#     db: Session = Depends(get_db),
#     current_user=Depends(get_current_user)
# ):
#     user_id = _user_id(current_user)

#     records = (
#         db.query(ProgressLog)
#         .filter(ProgressLog.user_id == user_id)
#         .order_by(ProgressLog.created_at.desc())
#         .all()
#     )

#     return records


@router.get("/skin-score/history")
def get_skin_score_history(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user_id = _user_id(current_user)

    records = (
        db.query(SkinScoreHistory)
        .filter(SkinScoreHistory.user_id == user_id)
        .order_by(SkinScoreHistory.created_at.desc())
        .all()
    )

    return [
        {
            "id": record.id,
            "skin_condition_score": record.skin_condition_score,
            "lifestyle_score": record.lifestyle_score,
            "sleep_score": record.sleep_score,
            "routine_score": record.routine_score,
            "hydration_score": record.hydration_score,
            "total_score": record.total_score,
            "created_at": record.created_at.isoformat()
            if record.created_at else None,
        }
        for record in records
    ]
