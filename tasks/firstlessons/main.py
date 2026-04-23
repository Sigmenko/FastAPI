from fastapi import FastAPI, HTTPException, Path
from typing import Optional, List, Dict, Annotated
from fastapi import status
from fastapi.params import Depends
from sqlalchemy.orm import Session
from models import Base,User,Post
from database import engine, session_local
from schemas import UserCreate, User as DbUser,PostCreate, PostResponse
app = FastAPI()


Base.metadata.create_all(bind=engine)
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

@app.post('/users/', response_model=DbUser)
async def add_user(user: UserCreate, db: Session = Depends(get_db)) -> DbUser:
    db_user = User(name=user.name, age=user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@app.post('/posts/', response_model=PostResponse)
async def add_user(post: PostCreate, db: Session = Depends(get_db)) -> PostResponse:
    db_user = db.query(User).filter(User.id == post.author_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found ')
    db_post = Post(title= post.title, body= post.body, author_id= post.author_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post

@app.get('/posts', response_model=List[PostResponse])
async def get_posts(db: Session = Depends(get_db)):
    return db.query(Post).all()