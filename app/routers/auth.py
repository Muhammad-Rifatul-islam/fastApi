from fastapi import APIRouter,status,Depends,HTTPException,responses

from sqlalchemy.orm import Session
from .. import database,schemas,utils,models,oauth2
from datetime import timedelta

router=APIRouter(tags=["Authentication"])



@router.post("/login")
def login(userCredential:schemas.UserLogin,db:Session=Depends(database.get_db)):

    user=db.query(models.User).filter(models.User.email==userCredential.email).first()

    if not user: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Credential")
    
    if not utils.verify_password(userCredential.password,user.password):
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Credential")
    
    access_token=oauth2.create_access_token(
        data={"user_id" :  user.id},
        expires_delta=timedelta(minutes=oauth2.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token,"token_type":"bearer"}

