from fastapi import FastAPI, Body, APIRouter, Request
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
        statement = "insert into users (user_name,age,gender,book_limit,fine_amount,status) values ('{}', {}, '{}', 5, 0, 1)".format(user_data['user_name'], int(user_data['age']), user_data['gender'])
        cursor.execute(statement)
        connection.commit()
        return "user {} Created".format(user_data['user_name'])
    except Exception as e:
        return "user Not Created"

@router.post("/edit_user")
async def edit_user(user_data:Dict = Body(...)):
    user_data = jsonable_encoder(user_data)
    try:
        cursor = connection.cursor()
        statement = "update users set user_name = '{}',age= {}, gender='{}' where user_id = {}".format(user_data['user_name'],int(user_data['age']),user_data['gender'],user_data['user_id'])
        cursor.execute(statement)
        connection.commit()
        return "User {} Updated".format(user_data['user_name'])
    except Exception as e:
        return "User Not Updated"


@router.get("/delete_user/{user_id}")
async def delete_user(user_id):
   try:
       cursor = connection.cursor()
       statement = "delete from users where user_id = {}".format(int(user_id))
       cursor.execute(statement)
       connection.commit()
       return "User {} Deleted successfully".format(user_id)
   except Exception as e:
       return "User Not Deleted"

@router.get("/get_users/{user_id}/{status}")
async def get_users(request: Request,user_id = -1, status = 0):
    try:
        if status == 0:
            cursor = request.app.mysql.cursor()
            if int(user_id) == -1:
                statement = "select * from users"
                cursor.execute(statement)

                rows = cursor.fetchall()
                users = []
                for row in rows:
                    users.append(
                        dict(zip(['user_id', 'user_name', 'age', 'gender', 'book_limit', 'fine_amount', 'status'], row)))
                return users
            else:
                statement = "select * from users where user_id = {}".format(int(user_id))
                cursor.execute(statement)
                rows = cursor.fetchone()
                if rows:
                    return dict(zip(['user_id', 'user_name', 'age', 'gender', 'book_limit', 'fine_amount', 'status'], rows))
                else:
                    return "User not found"
        else:
            cursor = request.app.mysql.cursor()
            statement = "select * from users where status = 1"
            cursor.execute(statement)

            rows = cursor.fetchall()
            users = []
            for row in rows:
                users.append(
                    dict(
                        zip(['user_id', 'user_name', 'age', 'gender', 'book_limit', 'fine_amount', 'status'], row)))
            return users

    except Exception as e:
        return "Something went wrong"












