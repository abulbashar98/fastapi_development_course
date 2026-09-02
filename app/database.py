from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings


# SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address>:<port>/database_name"

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost/database_name"

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_ip_address}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

sessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()


def get_db():

    db = sessionLocal()

    try:
        yield db
    finally:
        db.close()




# while True:
#     try:
#         conn = psycopg2.connect(host = "localhost", dbname = "Fastapi", user = "postgres", password = "password1234",cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connected successfully!!")
#         break

#     except Exception as error:
#         print("Database connection failed")
#         print("Error: ", error)
#         time.sleep(2)