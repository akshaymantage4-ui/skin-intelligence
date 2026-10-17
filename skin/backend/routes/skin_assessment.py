from models.skincare_routine import SkincareRoutine
from services.skin_score import calculate_skin_score
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.skin_assessment import SkinAssessment
from models.lifestyle_profile import LifestyleProfile
from models.sleep_log import SleepLog
from models.environment_profile import EnvironmentProfile

from schemas.skin_assessment import (
    SkinAssessmentCreate,
    SkinAssessmentResponse
)

from routes.auth import get_current_user

from services.skin_assessment_engine import analyze_skin_assessment
from models.skin_score_history import SkinScoreHistory

router = APIRouter()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post(
    "/skin-assessment",
    response_model=SkinAssessmentResponse
)
def create_skin_assessment(
    assessment: SkinAssessmentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    user_id = current_user["id"]

    existing_assessment = db.query(SkinAssessment).filter(
        SkinAssessment.user_id == user_id
    ).first()

    if existing_assessment:
        raise HTTPException(
            status_code=400,
            detail="Skin assessment already exists"
        )

    new_assessment = SkinAssessment(
        user_id=user_id,
        skin_type=assessment.skin_type,
        acne_level=assessment.acne_level,
        dryness_level=assessment.dryness_level,
        pigmentation_level=assessment.pigmentation_level,
        sensitivity_level=assessment.sensitivity_level,
        additional_concerns=assessment.additional_concerns
    )

    db.add(new_assessment)
    db.commit()
    db.refresh(new_assessment)

    return new_assessment


@router.get(
    "/skin-assessment",
    response_model=SkinAssessmentResponse
)
def get_skin_assessment(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    user_id = current_user["id"]

    assessment = db.query(SkinAssessment).filter(
        SkinAssessment.user_id == user_id
    ).first()

    if assessment is None:
        raise HTTPException(
            status_code=404,
            detail="Skin assessment not found"
        )

    return assessment


@router.put(
    "/skin-assessment",
    response_model=SkinAssessmentResponse
)
def update_skin_assessment(
    assessment: SkinAssessmentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    user_id = current_user["id"]

    existing_assessment = db.query(SkinAssessment).filter(
        SkinAssessment.user_id == user_id
    ).first()

    if existing_assessment is None:
        raise HTTPException(
            status_code=404,
            detail="Skin assessment not found"
        )

    existing_assessment.skin_type = assessment.skin_type
    existing_assessment.acne_level = assessment.acne_level
    existing_assessment.dryness_level = assessment.dryness_level
    existing_assessment.pigmentation_level = assessment.pigmentation_level
    existing_assessment.sensitivity_level = assessment.sensitivity_level
    existing_assessment.additional_concerns = assessment.additional_concerns

    db.commit()
    db.refresh(existing_assessment)

    return existing_assessment


@router.get("/skin-assessment/analysis")
def get_skin_analysis(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    user_id = current_user["id"]

    assessment = db.query(SkinAssessment).filter(
        SkinAssessment.user_id == user_id
    ).first()

    if assessment is None:
        raise HTTPException(
            status_code=404,
            detail="Skin assessment not found"
        )

    lifestyle = db.query(LifestyleProfile).filter(
        LifestyleProfile.user_id == user_id
    ).first()

    sleep_logs = db.query(SleepLog).filter(
        SleepLog.user_id == user_id
    ).all()

    environment = db.query(EnvironmentProfile).filter(EnvironmentProfile.user_id == user_id).first()

    analysis = analyze_skin_assessment(
        assessment=assessment,
        lifestyle=lifestyle,
        sleep_logs=sleep_logs,
        environment=environment
    )

    return analysis


@router.get("/skin-score")
def get_skin_score(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user_id = current_user["id"]

    assessment = (
        db.query(SkinAssessment)
        .filter(SkinAssessment.user_id == user_id)
        .first()
    )

    if assessment is None:
        raise HTTPException(
            status_code=404,
            detail="Please complete skin assessment first"
        )

    lifestyle = (
        db.query(LifestyleProfile)
        .filter(LifestyleProfile.user_id == user_id)
        .first()
    )

    sleep_logs = (
        db.query(SleepLog)
        .filter(SleepLog.user_id == user_id)
        .all()
    )

    routine = (
        db.query(SkincareRoutine)
        .filter(SkincareRoutine.user_id == user_id)
        .first()
    )

    score = calculate_skin_score(
        assessment=assessment,
        lifestyle=lifestyle,
        sleep_logs=sleep_logs,
        routine=routine
    )

    history = SkinScoreHistory(
        user_id=user_id,
        total_score=score["total_score"],
        skin_condition_score=score["skin_condition_score"],
        lifestyle_score=score["lifestyle_score"],
        sleep_score=score["sleep_score"],
        routine_score=score["routine_score"],
        hydration_score=score["hydration_score"]
    )

    db.add(history)
    db.commit()
    db.refresh(history)

    return score

@router.get("/skin-score-history")
def get_skin_score_history(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user_id = current_user["id"]

    history = (
        db.query(SkinScoreHistory)
        .filter(SkinScoreHistory.user_id == user_id)
        .order_by(SkinScoreHistory.created_at.desc())
        .all()
    )

    return history


