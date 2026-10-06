from fastapi import FastAPI,Response,status,HTTPException,Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import models, schema, util
from .database import engine, get_db
from.routers import post, users, authenticate,vote
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(post.router)
app.include_router(users.router)
app.include_router(authenticate.router)
app.include_router(vote.router)

#while True:
#    try:
#       conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='Runt0wn123', cursor_factory=RealDictCursor)
#       cur = conn.cursor()
#        print("Database connection was successful")
#        break
#   except Exception as e:
#      print(f"Error connecting to PostgreSQL: {e}")


@app.get("/")
async def root():
    return {"message": "Hellofefefd World"}






    