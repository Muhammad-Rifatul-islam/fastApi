from fastapi import FastAPI,Depends
from pydantic import BaseModel,HttpUrl

from . import models
from .database import engine,Base,get_db

from sqlalchemy.orm import session




app =FastAPI()

#create table

models.Base.metadata.create_all(bind=engine)

 


class Course(BaseModel):
   
   name :str
   instructor: str
   duration : float
   website: HttpUrl


student = {
    "name": "Rifat",
    "course": "FastAPI"
}
 
@app.get("/")
def greet():

   return student

@app.post("/post")
def create_post(post:Course):
   
    print(post)
    return { "data":post}


@app.get("/course")
def dbCheck(db:session=Depends(get_db)):
   return "Alchecmy works"