from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db 
from .. import schemas, models, utils

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

# create user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hash the password in user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())

    # add and commit changes to db
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# get a user
@router.get("/{id}", response_model=schemas.UserResponse)
async def get_user(id: int, db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'User with ID: {id} not found.')
    
    return user