from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
#----------------
# from urllib.parse import quote_plus
DATABASE_URL=URL.create(drivername="postgresql+psycopg2",
                        username="postgres",
                        password="Akshay@123",
                        host='localhost',
                        port=5432,
                        database='skin_intelligence'
                        )
engine=create_engine(DATABASE_URL)
SessionLocal=sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
Base=declarative_base()

if __name__=="__main__":
    try:
        with engine.connect() as connection:
            print("Postgresql connection successful")
    except Exception as e:
        print("Database connection failed:")
        print(e)
