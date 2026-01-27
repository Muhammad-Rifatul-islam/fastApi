from fastapi import APIRouter,status,Depends,HTTPException,responses

from sqlalchemy.orm import Session
from .. import database,schemas,utils,models

router=APIRouter(tags=["Authentication"])



@router.post("/login")
def login(userCredential:schemas.UserLogin,db:Session=Depends(database.get_db)):

    user=db.query(models.User).filter(models.User.email==userCredential.email).first()

    if not user: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Credential")
    
    if not utils.verify_password(userCredential.password,user.password):
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Credential")
    
    return {"Token": "Succcesfully login"}