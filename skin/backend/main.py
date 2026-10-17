from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine

# Import every model before create_all so SQLAlchemy knows every M1-M3 table.
from models.user import User
from models.user_profile import UserProfile
from models.skin_profile import SkinProfile
from models.lifestyle_profile import LifestyleProfile
from models.environment_profile import EnvironmentProfile
from models.sleep_log import SleepLog
from models.skin_assessment import SkinAssessment
from models.skincare_routine import SkincareRoutine
from models.skin_score_history import SkinScoreHistory
from models.ingredient_analysis import IngredientAnalysisHistory
from models.product import Product
from models.product_recommendation import ProductRecommendationHistory
from models.progress_log import ProgressLog

from routes.auth import router as auth_router
from routes.profile import router as profile_router
from routes.skin_profile import router as skin_profile_router
from routes.lifestyle_profile import router as lifestyle_router
from routes.environment_profile import router as environment_router
from routes.sleep_tracking import router as sleep_router
from routes.skin_assessment import router as skin_assessment_router
from routes.skincare_routine import router as skincare_routine_router
from routes.milestone3 import router as milestone3_router
from seed import seed_products

app = FastAPI(
    title="AI Skin Intelligence & Personalized Skincare API",
    description="M1-M3 FastAPI backend with PostgreSQL persistence",
    version="3.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
seed_products()

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(profile_router, prefix="/user", tags=["User Profile"])
app.include_router(skin_profile_router, prefix="/user", tags=["Skin Profile"])
app.include_router(lifestyle_router, prefix="/user", tags=["Lifestyle Profile"])
app.include_router(environment_router, prefix="/user", tags=["Environment Profile"])
app.include_router(sleep_router, prefix="/user", tags=["Sleep Tracking"])
app.include_router(skin_assessment_router, prefix="/user", tags=["Skin Assessment"])
app.include_router(skincare_routine_router, prefix="/user", tags=["Skincare Routine"])
app.include_router(milestone3_router, prefix="/user", tags=["Milestone 3"])

@app.get("/")
def home():
    return {"message": "Skin Intelligence API is running", "milestone": "M1-M3"}

@app.get("/about")
def about():
    return {"project": "AI Skin Intelligence & Personalized Skincare", "version": "3.0.0", "database": "PostgreSQL"}
