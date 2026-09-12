from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.sleep_log import SleepLog

from schemas.sleep_log import (
    SleepLogCreate,
    SleepLogResponse
)

from routes.auth import get_current_user


router = APIRouter()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# =========================
# CREATE SLEEP LOG
# =========================

@router.post(
    "/sleep",
    response_model=SleepLogResponse
)
def create_sleep_log(
    sleep: SleepLogCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    existing_log = db.query(SleepLog).filter(
        SleepLog.user_id == current_user["id"],
        SleepLog.sleep_date == sleep.sleep_date
    ).first()

    if existing_log:

        raise HTTPException(
            status_code=400,
            detail="Sleep log already exists for this date"
        )


    new_log = SleepLog(

        user_id=current_user["id"],

        sleep_date=sleep.sleep_date,

        sleep_duration=sleep.sleep_duration,

        sleep_quality=sleep.sleep_quality

    )

    db.add(new_log)

    db.commit()

    db.refresh(new_log)

    return new_log


# =========================
# GET SLEEP HISTORY
# =========================

@router.get(
    "/sleep",
    response_model=list[SleepLogResponse]
)
def get_sleep_history(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    sleep_logs = db.query(SleepLog).filter(
        SleepLog.user_id == current_user["id"]
    ).order_by(
        SleepLog.sleep_date.desc()
    ).all()

    return sleep_logs