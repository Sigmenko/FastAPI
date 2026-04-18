from fastapi import FastAPI, HTTPException
from typing import Optional, List, Dict
from pydantic import BaseModel
app = FastAPI()

class Users(BaseModel):
    id: int
    name: str
    age: int

class Post(BaseModel):
    id: int
    title: str
    body: str
    author: Users

#запуск сервера
#uvicorn - сервер #main:app - файл в якому находиться обєкт який ми створили # --reload - при якійсь змінні сервер перезапускається

users = [
    {'id': 1, 'name': 'Bob', 'age': 18},
    {'id': 2, 'name': 'Alex', 'age': 19},
    {'id': 3, 'name': 'Gosha', 'age': 20},
    {'id': 4, 'name': 'Olena', 'age': 17}
]
posts = [
    {'id': 1, 'title': 'Name book 1 ', 'body':'internal text 1', 'author': users[0]},
    {'id': 2, 'title': 'Name book 2 ', 'body':'internal text 2', 'author': users[1]},
    {'id': 3, 'title': 'Name book 3 ', 'body':'internal text 3', 'author': users[2]},
    {'id': 3, 'title': 'Name book 3 ', 'body':'internal text 33', 'author': users[3]},
    {'id': 4, 'title': 'Name book 4 ', 'body':'internal text 4', 'author': users[3]}
]

@app.get("/items")
async def items() -> List[Post]:
    return [Post(**post) for post in posts]


@app.get("/items/{id}")
async def items(id:int) -> Post:
    for post in posts:
        if post['id'] == id:
            return Post(**post)

    raise HTTPException(status_code=404, detail="Post not found")

@app.get('/search')
async def search(post_id: Optional[int] = None) -> Dict[str, Optional[Post]]:

    if post_id is None:
        return {'data': None}

    for post in posts:
        if post['id'] == post_id:
            return {"data": Post(**post)}
    raise HTTPException(status_code=404, detail="Post not found")

@app.get("/users")
async def allUsers() -> List[Users]:
    return [Users(**user) for user in users]

@app.get("/users/{id}")
async def allUsers(id:int) -> Users:
    for user in users:
        if user['id'] == id:
            return Users(**user)

@app.get("/users/{id}/posts")
async def get_user_post(id: int) -> List[Post]:
    founded_posts = []
    for post in posts:
        if post['author']['id'] == id:
            founded_posts.append(Post(**post))

    return founded_posts
