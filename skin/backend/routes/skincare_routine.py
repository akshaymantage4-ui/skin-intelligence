from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.skin_assessment import SkinAssessment
from models.lifestyle_profile import LifestyleProfile
from models.skincare_routine import SkincareRoutine
from models.sleep_log import SleepLog

from routes.auth import get_current_user

from services.skin_assessment_engine import analyze_skin_assessment
from services.skincare_routine_generator import generate_skincare_routine

from schemas.skincare_routine import SkincareRoutineResponse


router = APIRouter()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post(
    "/skincare-routine",
    response_model=SkincareRoutineResponse
)
def create_skincare_routine(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    user_id = current_user["id"]

    # Get skin assessment
    assessment = db.query(SkinAssessment).filter(
        SkinAssessment.user_id == user_id
    ).first()

    if assessment is None:
        raise HTTPException(
            status_code=404,
            detail="Please complete skin assessment first"
        )

    # Get lifestyle profile
    lifestyle = db.query(LifestyleProfile).filter(
        LifestyleProfile.user_id == user_id
    ).first()

    sleep_logs = db.query(SleepLog).filter(SleepLog.user_id == user_id).all()

    # Analyze skin before generating an adaptive routine.
    analysis = analyze_skin_assessment(
        assessment=assessment,
        lifestyle=lifestyle,
        sleep_logs=sleep_logs
    )

    # Generate routine
    routine = generate_skincare_routine(
        assessment=assessment,
        lifestyle=lifestyle,
        analysis=analysis
    )

    # Check existing routine
    existing_routine = db.query(SkincareRoutine).filter(
        SkincareRoutine.user_id == user_id
    ).first()

    if existing_routine:

        existing_routine.morning_routine = "\n".join(
            routine["morning_routine"]
        )

        existing_routine.evening_routine = "\n".join(
            routine["evening_routine"]
        )

        existing_routine.weekly_routine = "\n".join(
            routine["weekly_routine"]
        )

        existing_routine.recommendations = "\n".join(
            routine["recommendations"]
        )

        db.commit()
        db.refresh(existing_routine)

        return existing_routine

    # Create new routine
    new_routine = SkincareRoutine(
        user_id=user_id,
        morning_routine="\n".join(
            routine["morning_routine"]
        ),
        evening_routine="\n".join(
            routine["evening_routine"]
        ),
        weekly_routine="\n".join(
            routine["weekly_routine"]
        ),
        recommendations="\n".join(
            routine["recommendations"]
        )
    )

    db.add(new_routine)
    db.commit()
    db.refresh(new_routine)

    return new_routine


@router.get(
    "/skincare-routine",
    response_model=SkincareRoutineResponse
)
def get_skincare_routine(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    user_id = current_user["id"]

    routine = db.query(SkincareRoutine).filter(
        SkincareRoutine.user_id == user_id
    ).first()

    if routine is None:
        raise HTTPException(
            status_code=404,
            detail="Skincare routine not found"
        )

    return routine


