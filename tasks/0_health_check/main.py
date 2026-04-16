from fastapi import FastAPI, HTTPException
from typing import Optional
app = FastAPI()
@app.get("/")
def home() -> dict:
    return {'id': [1,10]}

#запуск сервера
#uvicorn - сервер #main:app - файл в якому находиться обєкт який ми створили # --reload - при якійсь змінні сервер перезапускається
posts = [
    {'id': 1, 'tilte': 'Name book 1 ', 'body':'internal text 1'},
    {'id': 2, 'tilte': 'Name book 2 ', 'body':'internal text 2'},
    {'id': 3, 'tilte': 'Name book 3 ', 'body':'internal text 3'},
    {'id': 4, 'tilte': 'Name book 4 ', 'body':'internal text 4'}
]

@app.get("/items")
async def items() -> list:
    return posts

@app.get("/items/{id}")
async def items(id:int) -> dict:
    for post in posts:
        if post['id'] == id:
            return post

    raise HTTPException(status_code=404, detail="Post not found")

@app.get('/search')
async def search(post_id: Optional[int] = None) -> dict:

    if post_id is None:
        return {'data': 'Please specify post_id '}

    for post in posts:
        if post['id'] == post_id:
            return post
    raise HTTPException(status_code=404, detail="Post not found")

