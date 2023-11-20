from fastapi import FastAPI, Body, APIRouter
from typing import Dict
from fastapi.encoders import jsonable_encoder
import mysql.connector
import uvicorn

router = APIRouter()

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysql12",
    database="lms"
)

@router.post("/create_user")
async def create_user(user_data:Dict = Body(...)):
    user_data = jsonable_encoder(user_data)

    try:
        cursor = connection.cursor()
        statement = "insert into users (user_name,age,gender,book_limit,fine_amount,status) values ('{}', {}, '{}', 5, 0, 1)".format(user_data['user_name'], user_data['age'], user_data['gender'])
        cursor.execute(statement)
        connection.commit()
        return "user {} Created".format(user_data['user_name'])
    except Exception as e:
        return "user Not Created"


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)