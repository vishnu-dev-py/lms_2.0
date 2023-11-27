from fastapi import FastAPI, Body, APIRouter, Request
from typing import Dict
from fastapi.encoders import jsonable_encoder

import arrow
import uvicorn



router = APIRouter()

def calculate_fine(issue_date,return_date):
    days = ((arrow.get(return_date, 'YYYY-MM-DD') - arrow.get(issue_date)).days)

    if days > 5:
        return (days - 4) * 10
    else:
        return 0

@router.post("/issue_book")
async def issue_book(request: Request,issue_data:dict=Body(...)):
    issue_data = jsonable_encoder(issue_data)
    try:
        cursor = request.app.mysql.cursor()
        statement = "insert into issue (user_id, book_id, issue_date, return_date, status) values ('{}', '{}', '{}', null, 1)".\
            format(issue_data['user_id'], issue_data['book_id'], issue_data['issue_date'])
        cursor.execute(statement)
        request.app.mysql.commit()

        statement = "update users set status = 0 where user_id = '{}'".format(issue_data['user_id'])
        cursor.execute(statement)
        request.app.mysql.commit()

        statement = "update books set availability = 0 where book_id = '{}'".format(issue_data['book_id'])
        cursor.execute(statement)
        request.app.mysql.commit()
        cursor.close()

        return "Book Issued!"
    except Exception as e:
        return "Error on issue book"
    return "Inprogress"


@router.get("/get_issue_items")
async def get_issue_items(request: Request):
    try:
        cursor = request.app.mysql.cursor()
        statement = "select i.issue_id, b.book_title, u.user_name, i.issue_date, i.status from issue i " \
                    "join books b on i.book_id = b.book_id " \
                    "join users u on i.user_id = u.user_id"
        cursor.execute(statement)
        rows = cursor.fetchall()
        items = []
        if rows:
            for row in rows:
                items.append(dict(zip(['issue_id', 'user_name', 'book_name', 'issue_date', 'status'], row)))

            return items
        else:
            return "No Issued items"

    except Exception as e:
        return "Error getting issued items"

@router.get("/return_book/{issue_id}/{return_date}")
async def return_book(request : Request, issue_id, return_date):
    try:
        cursor = request.app.mysql.cursor()
        statement = "select * from issue where issue_id = '{}'".format(issue_id)
        cursor.execute(statement)
        issue = cursor.fetchone()

        fine_amount = calculate_fine(issue[3],return_date)

        statement = "update issue set return_date = '{}', status = 0, fine = {} where issue_id = '{}'".format(return_date, fine_amount,issue_id)
        cursor.execute(statement)
        request.app.mysql.commit()

        statement = "update users set status = 1 where user_id = '{}'".format(issue[1])
        cursor.execute(statement)
        request.app.mysql.commit()

        statement = "update books set availability = 1 where book_id = '{}'".format(issue[2])
        cursor.execute(statement)
        request.app.mysql.commit()

        return "Book returned!"
    except Exception as e:
        return "Error on returning a book"
