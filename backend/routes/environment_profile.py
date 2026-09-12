from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.environment_profile import EnvironmentProfile
from schemas.environment_profile import(
    EnvironmentProfileCreate,
    EnvironmentProfileResponse
)

#import your existing jwt authentication dependency
from routes.auth import get_current_user


router=APIRouter()

def get_db():
    db=SessionLocal()

    try:
        yield db
    finally:db.close()

@router.post(
    '/environment-profile',
    response_model=EnvironmentProfileResponse
)

def create_environment_profile(
    environment:EnvironmentProfileCreate,
    db:Session=Depends(get_db),
    current_user=Depends(get_current_user)
):


    new_environment=EnvironmentProfile(
        user_id=current_user['id'],
        location=environment.location,
        uv_index=environment.uv_index,
        pollution_level=environment.pollution_level,
        temperature=environment.temperature,
        water_quality=environment.water_quality
    )

    db.add(new_environment)
    db.commit()
    db.refresh(new_environment)

    return new_environment


@router.get(
    "/environment-profile",
    response_model=EnvironmentProfileResponse
)
def get_environment_profile(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    print("CURRENT USER:", current_user)

    user_id = current_user["id"]

    environment = db.query(EnvironmentProfile).filter(
        EnvironmentProfile.user_id == user_id
    ).first()

    print("ENVIRONMENT PROFILE:", environment)

    if environment is None:
        raise HTTPException(
            status_code=404,
            detail=f"Environment profile not found for user {user_id}"
        )

    return environment

