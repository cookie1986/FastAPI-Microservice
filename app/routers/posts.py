from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db 
from .. import schemas, models

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

# get all posts
@router.get("/", response_model=List[schemas.PostResponse])
async def get_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    # print(db.query(models.Post)) # this should print the SQL command

    return posts

# get a single post
@router.get("/{id}", response_model=schemas.PostResponse)
async def get_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f'Post with ID: {id} not found.')

    return post


# create a new post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):

    new_post = models.Post(**post.dict())

    # add and commit changes to db
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

# delete a post
@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with ID: {id} does not exist.')
    # delete post and commit changes
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# update a post
@router.put("/{id}", response_model=schemas.PostResponse)
async def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with ID: {id} does not exist.')
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()