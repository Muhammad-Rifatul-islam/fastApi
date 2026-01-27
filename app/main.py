
from fastapi import FastAPI

from app.routers import user,course,auth
# from . import models
# from .database import engine,Base


app =FastAPI()


app.include_router(course.router)
app.include_router(user.router)
app.include_router(auth.router)

#models.Base.metadata.create_all(bind=engine)

 

