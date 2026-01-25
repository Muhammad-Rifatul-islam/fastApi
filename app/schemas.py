
from pydantic import BaseModel, HttpUrl

#for request schema 
class CreateCourse(BaseModel):
   
   name :str
   duration : float
   instructor: str
   website: HttpUrl

## for all field in response 
class CourseResponse(CreateCourse):
   id:int
   class Config:
      orm_model=True   

# ## for specific response
# class CourseResponse(BaseModel):
#    id:int
#    name:str
       