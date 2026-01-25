from fastapi import FastAPI,Depends,HTTPException,status
from pydantic import BaseModel,HttpUrl

from . import models
from .database import engine,Base,get_db

from sqlalchemy.orm import Session




app =FastAPI()

#create table

models.Base.metadata.create_all(bind=engine)

 


class Course(BaseModel):
   
   name :str
   duration : float
   instructor: str
   website: HttpUrl


student = {
    "name": "Rifat",
    "course": "FastAPI"
}
 
@app.get("/")
def greet():

   return student

# create a course
@app.post("/courses")
def create_post(course:Course,db:Session=Depends(get_db)):
   new_course=models.Course(
      name=course.name,
      duration=course.duration,
      instructor=course.instructor,
      website=str(course.website)
   )
   db.add(new_course)
   db.commit()
   db.refresh(new_course)
   return {"Course : ",new_course}


   
    
# Get all course

@app.get("/courses")
def get_courses(db:Session=Depends(get_db)):
    courses=db.query(models.Course).all()
    return courses

@app.get("/courses/{id}")
def get_courseByid(id:int,db:Session=Depends(get_db)):
   
   course=db.query(models.Course).filter(models.Course.id==id).first()
   if not course:
      raise HTTPException(
         status_code=status.HTTP_404_NOT_FOUND,
         detail= f"Course With Id:{id} was not found"
      )
   return "course_details:{course}"


# @app.put("/courses/{id}")
# def update_course(id:int,update_corse:Course,db:Session=Depends(get_db)):

#     course=db.query(models.Course).filter(models.Course.id==id).first()
    
#     if not course:
#        raise HTTPException(
#           status_code=status.HTTP_404_NOT_FOUND,
#           detail=f"Course with Id:{id} was not found"
#        )
#     update_data=update_corse.model_dump()
#     update_data["website"]=str( update_data["website"])
#     course.update(update_data,synchronize_session)
#     db.commit()
#     db.refresh(course)


 # update course      
@app.put("/courses/{id}")
def update_course(id: int, update_course: Course, db: Session = Depends(get_db)):
    db_course = db.query(models.Course).filter(models.Course.id == id).first()

    if not db_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "code": status.HTTP_404_NOT_FOUND,
                "message": f"Course with Id:{id} was not found",
              
            }
        )

    # Convert Pydantic to dict, only use provided fields
    update_data = update_course.model_dump(exclude_unset=True)

    # Convert HttpUrl to str if present
    if "website" in update_data:
     update_data["website"] = str(update_data["website"])

    for key, value in update_data.items():
        setattr(db_course, key, value)

    db.commit()
    db.refresh(db_course)

    return {
        "success": True,
        "code": 200,
        "message": "Course updated successfully",
        "data": db_course
    }
