import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://study:study@localhost:5435/auth_db",
)
JWT_SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "development-only-change-me-at-least-32-bytes",
)
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
