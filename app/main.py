"""
main
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
#from . import models
#from .database import engine
from .routers import posts, users, auth, vote

# tells sqlalechmy to create generrate all the tables (if they don't exist) when starting up
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    """Basic Hello World Route"""
    return {"message": "Hello Word!??!"}
