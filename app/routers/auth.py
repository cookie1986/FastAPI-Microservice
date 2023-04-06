from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..schemas import UserLogin
from ..database import get_db
from ..models import User
from .. import utils, oauth2

router = APIRouter(tags=['Authentication'])

@router.post("/login")
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    user = db.query(User).filter(User.email == user_credentials.username).first()

    # if email is incorrect
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail='Invalid credentials')
    
    # if password is incorrect
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail='Invalid credentials')
    
    # create access token
    access_token = oauth2.create_acess_token(data={"user_id": user.id})
    
    return{"access_token":access_token, "token_type": "bearer"}