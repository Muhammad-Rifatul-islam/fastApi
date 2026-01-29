


from typing import List
from fastapi import FastAPI,Depends,HTTPException,status,APIRouter
from app import models, schemas
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app import oauth2

router=APIRouter(
     prefix="/courses",
    tags=["Courses"]
)

@router.post("/",response_model=schemas.CourseResponse)
def create_post(course:schemas.CreateCourse,db:Session=Depends(get_db),get_current_user:int=Depends(oauth2.get_current_user)):
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

@router.get("/",response_model=List[schemas.CourseResponse])
def get_courses(db:Session=Depends(get_db),get_current_user:int=Depends(oauth2.get_current_user)):
    courses=db.query(models.Course).all()
    return courses

@router.get("/{id}",response_model=schemas.CourseResponse)
def get_courseByid(id:int,db:Session=Depends(get_db),get_current_user:int=Depends(oauth2.get_current_user)):
   
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
@router.put("/{id}",response_model=schemas.CourseResponse)
def update_course(id: int, update_course: schemas.CreateCourse, db: Session = Depends(get_db),get_current_user:int=Depends(oauth2.get_current_user)):
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
    

@router.delete("/{id}",status_code=status.HTTP_200_OK)
def deleteCourse(id:int,db:Session=Depends(get_db),get_current_user:int=Depends(oauth2.get_current_user) ):
   
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

