from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .database import engine
from . import models
from .routers import posts, users





app = FastAPI()


models.Base.metadata.create_all(bind=engine)


app.include_router(posts.router)
app.include_router(users.router)


while True:
    try:
        conn = psycopg2.connect(host = "localhost", dbname = "Fastapi", user = "postgres", password = "password1234",cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connected successfully!!")
        break

    except Exception as error:
        print("Database connection failed")
        print("Error: ", error)
        time.sleep(2)




# request get Method url ("/")
@app.get("/")
def root():
    return {"message": "Hello World!"}






