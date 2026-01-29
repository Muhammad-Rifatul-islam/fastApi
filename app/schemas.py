
from typing import Optional
from pydantic import BaseModel, EmailStr, HttpUrl
from datetime import datetime

#for request schema 
class CreateCourse(BaseModel):
   
   name :str
   duration : float
   instructor: str
   website: HttpUrl

## for all field in response 
class CourseResponse(CreateCourse):
   id:int
   creator_id:int
   class Config:
      orm_model=True   

# ## for specific response
# class CourseResponse(BaseModel):
#    id:int
#    name:str


class UserCreate(BaseModel):

   email:EmailStr
   password:str

class UserResponse(BaseModel):

   id :int
   email:EmailStr
   created_at:datetime

   class Config:
      orm_model=True

 
class UserLogin(BaseModel):

   email: EmailStr
   password: str


class Token(BaseModel):
   access_token: str
   token_type: str

class TokenData(BaseModel):
   id :Optional[int]= None