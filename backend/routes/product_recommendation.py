from typing import Optional
from fastapi import APIRouter,Depends,HTTPException,Query
from sqlalchemy.orm import Session
from database import SessionLocal
from dependencies.auth import get_current_user

from models.user import User
from models.product import Product
from models.skin_profile import SkinProfile
from models.skin_assessment import SkinAssessment
from services.product_recommendation import recommend_products
router=APIRouter()

def get_db():
    db=SessionLocal()
    try:
        yield db

    finally:
        db.close()
@router.get('/product-recommendation')
def get_product_recommendations(
    budget:Optional[float]=Query(default=None,ge=0),
    category:Optional[str]=None,
    db:Session=Depends(get_db),
    current_user:User=Depends(get_current_user)
):
    #1.get the logged-in user's skin profile
    profile=db.query(SkinProfile).filter(
        SkinProfile.user_id==current_user.id
    ).first()

    if not profile:
        raise HTTPException(
            status_code=404,
            detail='please create your skin profile first'
        )
    #2.Collect concerns from the skin profile
    concerns=[]
    if profile.acne:
        concerns.append('acne')

    if profile.dryness:
        concerns.append('dryness')
    if profile.pigmentation:
        concerns.append('pigmentation')

    if profile.sensitivity:
        concerns.append('sensitivity')

    #3. include concernms from the latest assessment,if available
    assessment=db.query(SkinAssessment).filter(
        SkinAssessment.user_id==current_user.id
    ).order_by(
        SkinAssessment.id.desc()
    ).first()

    if assessment:
        if assessment.additional_concerns:
            concerns.extend(
                concern.strip()
                for concern in assessment.additional_concerns.split(',')
                if concern.strip()
            )
        if assessment.acne_level:
            concerns.append('acne')
        if assessment.dryness_level:
            concerns.append('dryness')
        if assessment.pigmentation_level:
            concerns.append('pigmentation')

        if assessment.sensitivity_level:
            concerns.append('sensitivity')

    #4.get active products
    query=db.query(Product).filter(
        Product.is_active==True
    )

    if category:
        query=query.filter(
            Product.category.ilike(category.strip())
        )
    products=query.all()

    #5.generate recommendations

    results=recommend_products(
        products=products,
        skin_type=profile.skin_type,
        concerns=concerns,
        allergies=[],
        budget=budget
    )

    return{
        'skin_type':profile.skin_type,
        'concerns':list(set(concerns)),
        'count':len(results),
        "recommendations": [
    {
        "id": item["product"].id,
        "name": item["product"].name,
        "brand": item["product"].brand,
        "category": item["product"].category,
        "price": item["product"].price,
        "description": item["product"].description,
        "ingredients": item["product"].ingredients,
        "suitability_score": item["suitability_score"],
    }
    for item in results
]
    }