import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://study:study@localhost:5433/study_db",
)

