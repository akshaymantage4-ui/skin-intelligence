from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.lifestyle_profile import LifestyleProfile

from schemas.lifestyle_profile import (
    LifestyleProfileCreate,
    LifestyleProfileResponse
)

from routes.auth import get_current_user


router = APIRouter()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# CREATE
@router.post(
    "/lifestyle-profile",
    response_model=LifestyleProfileResponse
)
def create_lifestyle_profile(
    lifestyle: LifestyleProfileCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    existing_profile = db.query(LifestyleProfile).filter(
        LifestyleProfile.user_id == current_user["id"]
    ).first()

    if existing_profile:
        raise HTTPException(
            status_code=400,
            detail="Lifestyle profile already exists"
        )

    new_profile = LifestyleProfile(
        user_id=current_user["id"],
        sleep_hours=lifestyle.sleep_hours,
        water_intake=lifestyle.water_intake,
        exercise_days=lifestyle.exercise_days,
        stress_level=lifestyle.stress_level,
        smoking=lifestyle.smoking,
        alcohol=lifestyle.alcohol,
        sun_exposure_hours=lifestyle.sun_exposure_hours
    )

    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    return new_profile


# GET
@router.get(
    "/lifestyle-profile",
    response_model=LifestyleProfileResponse
)
def get_lifestyle_profile(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    lifestyle = db.query(LifestyleProfile).filter(
        LifestyleProfile.user_id == current_user["id"]
    ).first()

    if lifestyle is None:
        raise HTTPException(
            status_code=404,
            detail="Lifestyle profile not found"
        )

    return lifestyle


# UPDATE
@router.put(
    "/lifestyle-profile",
    response_model=LifestyleProfileResponse
)
def update_lifestyle_profile(
    lifestyle: LifestyleProfileCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    existing_profile = db.query(LifestyleProfile).filter(
        LifestyleProfile.user_id == current_user["id"]
    ).first()

    if existing_profile is None:
        raise HTTPException(
            status_code=404,
            detail="Lifestyle profile not found"
        )

    existing_profile.sleep_hours = lifestyle.sleep_hours
    existing_profile.water_intake = lifestyle.water_intake
    existing_profile.exercise_days = lifestyle.exercise_days
    existing_profile.stress_level = lifestyle.stress_level
    existing_profile.smoking = lifestyle.smoking
    existing_profile.alcohol = lifestyle.alcohol
    existing_profile.sun_exposure_hours = lifestyle.sun_exposure_hours

    db.commit()
    db.refresh(existing_profile)

    return existing_profile