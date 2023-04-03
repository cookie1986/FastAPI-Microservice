from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()




# schema for incoming posts
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


# set root endpoint
@app.get("/")
async def root():
    return {"message":"App and running!"}

# CRUD
# get all posts
@app.get("/posts")
async def get_posts():
    return {"data":"this is your posts"}

# get a single post
@app.get("/posts/{id}")
async def get_post(id: int, response: Response):

    return {"post_detail":f"here is post: {id}"}


# create a new post
@app.post("/createposts", status_code=status.HTTP_201_CREATED)
# async def create_posts(payload: dict = Body(...)): # old version, using pydantic to evaluate incoming posts
async def create_posts(post: Post):
    print(post.dict())
    return {"new_post":post}


