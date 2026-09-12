
from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.skin_profile import SkinProfile
from schemas.skin_profile import SkinProfileCreate, SkinProfileResponse

from dependencies.auth import get_current_user
from models.user import User


router = APIRouter()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post(
    "/skin-profile",
    response_model=SkinProfileResponse
)
def create_skin_profile(
    skin_profile: SkinProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    new_profile = SkinProfile(
        user_id=current_user.id,
        skin_type=skin_profile.skin_type,
        acne=skin_profile.acne,
        dryness=skin_profile.dryness,
        pigmentation=skin_profile.pigmentation,
        sensitivity=skin_profile.sensitivity
    )

    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    return new_profile


@router.get('/skin-profile',
            response_model=SkinProfileResponse
            )

def get_skin_profile(
    db:Session=Depends(get_db),
    current_user:User=Depends(get_current_user)
):

    profile=db.query(SkinProfile).filter(
        SkinProfile.user_id==current_user.id
    ).first()


    if not profile:
        raise HTTPException(
            status_code=404,
            detail='Skin Profile not found'
        )
    return profile


@router.put('/skin-profile',
            response_model=SkinProfileResponse)


def update_skin_profile(
    skin_profile:SkinProfileCreate,
    db:Session=Depends(get_db),
    current_user:User=Depends(get_current_user)
):
    profile=db.query(SkinProfile).filter(
        SkinProfile.user_id==current_user.id

    ).first()


    if not profile:
        raise HTTPException(
            status_code=404,
            detail='skin profile not found'
        )


    profile.skin_type=skin_profile.skin_type
    profile.acne=skin_profile.acne
    profile.dryness=skin_profile.dryness
    profile.pigmentation=skin_profile.pigmentation
    profile.sensitivity=skin_profile.sensitivity

    db.commit()
    db.refresh(profile)

    return profile

