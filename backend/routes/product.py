from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from dependencies.auth import get_current_user
from models.user import User
from models.product import Product
from schemas.product import ProductCreate,ProductResponse

router=APIRouter()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/products",response_model=ProductResponse)
def create_product(
    product_data:ProductCreate,
    db:Session=Depends(get_db),
    current_user:User=Depends(get_current_user)
):
    if current_user.role!='admin':
        raise HTTPException(
            status_code=403,
            detail='only admin can add products'

        )
    new_product=Product(
        name=product_data.name,
        brand=product_data.brand,
        category=product_data.category,
        price=product_data.price,
        description=product_data.description,
        suitable_skin_types=product_data.suitable_skin_types,
        target_concerns=product_data.target_concerns,
        ingredients=product_data.ingredients,
        avoids_allergies=product_data.avoids_allergies,
        is_active=True
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

@router.get('/products')
def get_all_products(
    db:Session=Depends(get_db)
):
    products=db.query(Product).all()

    return[
        {
            'id':product.id,
            'name':product.name,
            'brand':product.brand,
            'category':product.category,
            'price':product.price,
            'description':product.description,
            'suitable_skin_types':product.suitable_skin_types,
            'target_concerns':product.target_concerns,
            'ingredients':product.ingredients,
            'avoid_allergies':product.avoids_allergies,
            'is_active':product.is_active

        }

        for product in products
    ]