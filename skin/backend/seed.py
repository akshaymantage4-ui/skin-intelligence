import csv
from pathlib import Path
from database import SessionLocal
from models.product import Product

DATA = Path(__file__).resolve().parent / "data" / "products_seed.csv"

def convert_to_list(value):
    if not value:
        return []

    return [
        item.strip()
        for item in value.split(",")
        if item.strip()
    ]
def seed_products():
    db = SessionLocal()

    try:
        if db.query(Product).count() > 0:
            print("Products already exist. Skipping seeding.")
            return

        with DATA.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):

                db.add(Product(
                    name=row["name"],
                    brand=row["brand"],
                    category=row["category"],
                    price=float(row["price"]),

                    skin_types=convert_to_list(row["skin_types"]),
                    concerns=convert_to_list(row["concerns"]),
                    key_ingredients=convert_to_list(
                        row["key_ingredients"]
                    ),

                    description=row["description"],
                    is_active=True
                ))

        db.commit()
        print("Products seeded successfully!")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()
