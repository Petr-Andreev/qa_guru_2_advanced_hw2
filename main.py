from fastapi import FastAPI, HTTPException
from typing import List
import json

from pydantic import ValidationError

from models.app_status import AppStatus
from models.user import User
from fastapi_pagination import Page, paginate, add_pagination
from http import HTTPStatus
import uvicorn

app = FastAPI()

users: List[User] = []


@app.get("/status", status_code=HTTPStatus.OK)
def status() -> AppStatus:
    return AppStatus(users=bool(users))


@app.on_event("startup")
async def startup_event():
    with open('users.json') as f:
        raw_users = json.load(f)
    try:
        global users
        users = [User(**user) for user in raw_users]
    except ValidationError as e:
        print(f"Validation error: {e}")


@app.get("/api/users/{user_id}", status_code=HTTPStatus.OK)
def get_user(user_id: int) -> User:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")
    if user_id > len(users):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return users[user_id - 1]


@app.get("/api/users/", response_model=Page[User])
def get_users() -> Page[User]:
    return paginate(users)


# Добавляем пагинацию к приложению
add_pagination(app)

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8002)
