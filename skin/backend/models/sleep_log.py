from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey
from database import Base


class SleepLog(Base):

    __tablename__ = "sleep_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    sleep_date = Column(
        Date,
        nullable=False
    )

    sleep_duration = Column(
        Float,
        nullable=False
    )

    sleep_quality = Column(
        String(20),
        nullable=False
    )