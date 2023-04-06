from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from . import schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# run openssl rand -hex 32 to generate a new secret key
SECRET_KEY = '6e3a380efaf26dd3bfb390ceb2992398bebf928ec614d9a441177fe4a7f6757a'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_acess_token(data: dict):
    
    to_encode = data.copy()
    expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expires})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    
    except JWTError:
        raise credentials_exception
    
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          details='Could not validate credentials',
                                          headers={"WWW-Authenticate":"Bearer"}
                                          )
    
    return verify_access_token(token, credentials_exception)
    
