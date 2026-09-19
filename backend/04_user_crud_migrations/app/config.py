import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://study:study@localhost:5434/user_db",
)

