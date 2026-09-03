from fastapi import FastAPI
from sqlalchemy.orm import Session
from database import engine, get_db
import models as models

from config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME)

@app.get("/")
def main():
    return {"message": "Hello World"}