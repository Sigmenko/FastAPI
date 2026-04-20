from fastapi import FastAPI, HTTPException
from typing import Optional, List, Dict
from pydantic import BaseModel
from fastapi import status
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

class SensorReading(BaseModel):
    sensor_id: int
    temperature: float
    status: str
class PostCreate(BaseModel):
    title: str
    body: str
    author_id: int

class UserCreate(BaseModel):
    name: str
    age: int

#запуск сервера
#uvicorn - сервер #main:app - файл в якому находиться обєкт який ми створили # --reload - при якійсь змінні сервер перезапускається
sensors = [
    {'sensor_id': 1, 'temperature': 34.2,'status': 'online'},
    {'sensor_id': 2, 'temperature': 35.0, 'status': 'online'},
    {'sensor_id': 3, 'temperature': 30.1, 'status': 'ofline'}

]
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

@app.post("/items/add")
async def add_items(post:PostCreate) -> Post:
    author = next((user for user in users if user['id'] == post.author_id),None)
    if not author:
        raise HTTPException(status_code=404, detail='Author not founded')

    new_post_id = len(posts) + 1
    new_post = {'id':new_post_id, 'title': post.title, 'body': post.body, 'author':author}
    posts.append(new_post)

    return Post(**new_post)

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
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

@app.get("/users")
async def allUsers() -> List[Users]:
    return [Users(**user) for user in users]

@app.post("/users/add")
async def add_users(user: UserCreate) -> Users:
    new_id_news = len(users) + 1
    new_users_age = user.age
    if new_users_age < 18:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Age users is too young  ")
    new_user = {'id': new_id_news, 'name':user.name, 'age':user.age}
    users.append(new_user)
    return Users(**new_user)



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
@app.get("/sensor")
async def sensor():
    return sensors

@app.post("/sensor/data")
async def check_sensor(reading:SensorReading):
    sensors.append(reading)
    if reading.temperature > 100:
        return {"alert": "Overheating!", "data": reading}
    else:
        return {'status':"ok", 'data':reading}
