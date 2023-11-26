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

@router.post("/add_book")
async def add_book(book_data:Dict = Body(...)):
    book_data = jsonable_encoder(book_data)
    try:
        cursor = connection.cursor()
        statement = "insert into books(book_title ,author ,stock, availability) values ('{}','{}', {}, 1)".format(book_data['book_title'], book_data['author'], int(book_data['stock']))
        cursor.execute(statement)
        connection.commit()
        return "Book {} Created".format(book_data['book_title'])
    except Exception as e:
        return "Book Not Created"


@router.get("/delete_book/{book_id}")
async def delete_book(book_id):
    try:
        cursor = connection.cursor()
        statement = "delete from books where book_id = {}".format(int(book_id))
        cursor.execute(statement)
        connection.commit()
        return "Book {} deleted".format(book_id)

    except Exception as e:
        return "Book not deleted"

@router.post("/edit_book")
async def edit_book(book_data:dict=Body(...)):
    book_data = jsonable_encoder(book_data)
    try:
        cursor = connection.cursor()
        statement = "update books set book_title = '{}', author = '{}' where book_id = {}".format(book_data['book_title'], book_data['author'], int(book_data['book_id']))
        cursor.execute(statement)
        connection.commit()
        return "Book {} edited".format(book_data['book_title'])
    except Exception as e:
        return "Book not edited"


    
@router.get("/get_books/{book_id}/{availability}")
async def get_books(book_id = -1,availability = 0):
    try:
        cursor = connection.cursor()
        if availability == 0:
            if int(book_id) == -1:
                statement = "select * from books"
                cursor.execute(statement)

                rows = cursor.fetchall()
                books = []
                for row in rows:
                    books.append(
                        dict(zip(['book_id', 'book_title', 'author', 'stock', 'availability'], row)))
                return books
            else:
                statement = "select * from books where book_id = {}".format(int(book_id))
                cursor.execute(statement)
                rows = cursor.fetchone()
                if rows:
                    return dict(zip(['book_id', 'book_title', 'author', 'stock', 'availability'], rows))
                else:
                    return "Book not found"
        else:
            statement = "select * from books where availability = {}".format(int(availability))
            cursor.execute(statement)
            rows = cursor.fetchall()
            books = []
            for row in rows:
                books.append(
                    dict(zip(['book_id', 'book_title', 'author', 'stock', 'availability'], row)))
            return books

    except Exception as e:
        return e



