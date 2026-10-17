import os
from dotenv import load_dotenv
load_dotenv()

# JWT — single source of truth. Override via env var in production.
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "skin-intelligence-secret-key")
ALGORITHM = "HS256"

# Database — single source of truth. Override via env vars in production.
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")  # set DB_PASSWORD before running
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "skin_intelligence")
