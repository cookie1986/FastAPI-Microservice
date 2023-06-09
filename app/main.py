from fastapi import FastAPI

from .routers import posts, users, auth
from .database import engine
from . import models


# connect to database
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)

# set root endpoint
@app.get("/")
async def root():
    return {"message":"App and running!"}