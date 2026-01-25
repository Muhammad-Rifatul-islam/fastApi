from typing import List
from fastapi import FastAPI,Depends,HTTPException,status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from . import models,schemas
from .database import engine,Base,get_db

from sqlalchemy.orm import Session




app =FastAPI()

#create table

models.Base.metadata.create_all(bind=engine)

 




student = {
    "name": "Rifat",
    "course": "FastAPI"
}
 
@app.get("/")
def greet():

   return student

# create a course
@app.post("/courses",response_model=schemas.CourseResponse)
def create_post(course:schemas.CreateCourse,db:Session=Depends(get_db)):
   new_course=models.Course(
      **course.model_dump() 
        ##model_dump() → Pydantic object → dict
        #** Dict unpack
   
   
    #   name=course.name,
    #   duration=course.duration,
    #   instructor=course.instructor,
    #   website=str(course.website)
   )
   new_course.website=str(course.website)
   db.add(new_course)
   db.commit()
   db.refresh(new_course)
   return new_course

   
    
# Get all course

@app.get("/courses",response_model=List[schemas.CourseResponse])
def get_courses(db:Session=Depends(get_db)):
    courses=db.query(models.Course).all()
    return courses

@app.get("/courses/{id}",response_model=schemas.CourseResponse)
def get_courseByid(id:int,db:Session=Depends(get_db)):
   
   course=db.query(models.Course).filter(models.Course.id==id).first()
   if not course:
      raise HTTPException(
         status_code=status.HTTP_404_NOT_FOUND,
         detail= f"Course With Id:{id} was not found"
      )
   return course


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
@app.put("/courses/{id}",response_model=schemas.CourseResponse)
def update_course(id: int, update_course: schemas.CreateCourse, db: Session = Depends(get_db)):
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

    return db_course
    

@app.delete("/course/{id}",status_code=status.HTTP_200_OK)
def deleteCourse(id:int,db:Session=Depends(get_db) ):
   
   course =db.query(models.Course).filter(models.Course.id ==id).first()

   if not course:
      
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail= f"No Course Found")
   db.delete(course)
   db.commit()

   return JSONResponse(
    status_code=status.HTTP_200_OK,
    content={"message": "Delete Successfully"}
)


#create user

@app.post("/users", status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        # Pydantic object → dict
        data = user.model_dump()
    
        new_user = models.User(**data)

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    except IntegrityError as e:
       
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )

    except Exception as e:
       
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error: {str(e)}"
        )