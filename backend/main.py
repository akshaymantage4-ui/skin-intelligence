
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine

from models.user import User
from models.user_profile import UserProfile
from models.skin_profile import SkinProfile
from models.lifestyle_profile import LifestyleProfile

from routes.auth import router as auth_router
from routes.profile import router as profile_router
from routes.skin_profile import router as skin_profile_router
from routes.lifestyle_profile import router as lifestyle_router
from routes.environment_profile import router as environment_router
from routes.sleep_tracking import router as sleep_router
from models.sleep_log import SleepLog
from routes.skin_assessment import router as skin_assessment_router
from routes.skincare_routine import router as skincare_routine_router
from models.skin_score_history import SkinScoreHistory
from models.product import Product
from routes.product import router as products_router

from routes.product_recommendation import (
    router as product_recommendations_router
)
app = FastAPI(
    title="Skin Intelligence API",
    description="AI-powered personalized skincare platform",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





# Create database tables
Base.metadata.create_all(bind=engine)


# Authentication routes
app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)


# User profile routes
app.include_router(
    profile_router,
    prefix="/user",
    tags=["User Profile"]
)


# Skin profile routes
app.include_router(
    skin_profile_router,
    prefix="/user",
    tags=["Skin Profile"]
)


# Lifestyle profile routes
app.include_router(
    lifestyle_router,
    prefix="/user",
    tags=["Lifestyle Profile"]
)


@app.get("/")
def home():
    return {
        "message": "Skin Intelligence API is running"
    }


@app.get("/about")
def about():
    return {
        "project": "AI Skin Intelligence & Personalized Skincare",
        "version": "1.0.0"
    }

# Environment profile routes
app.include_router(
    environment_router,
    prefix="/user",
    tags=["Environment Profile"]
)


app.include_router(sleep_router, prefix="/user")

app.include_router(
    skin_assessment_router,
    prefix="/user",
    tags=["Skin Assessment"]
)

app.include_router(
    skincare_routine_router,
    prefix="/user",
    tags=["Skincare Routine"]
)

app.include_router(
    product_recommendations_router,
    prefix="/user",
    tags=["Product Recommendations"]
)
app.include_router(
    products_router,
    prefix="/admin",
    tags=["Products"]
)