
from typing import List
from fastapi import FastAPI,Depends,HTTPException,status,APIRouter
from sqlalchemy.exc import IntegrityError
from app import models, schemas, utils
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse


router=APIRouter()

#create user

@router.post("/users", status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        hashed_password=utils.hash_password(user.password)
        user.password=hashed_password
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