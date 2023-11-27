from fastapi import FastAPI, Body, APIRouter, Request
from typing import Dict
from fastapi.encoders import jsonable_encoder
import mysql.connector
import uvicorn

router = APIRouter()

@router.get("/get_fine/{user_id}")
async def get_fine(request: Request, user_id):
    try:
        cursor = request.app.mysql.cursor()
        statement = "select sum(fine) from issue where user_id = '{}'".format(user_id)
        cursor.execute(statement)
        fine_amount = cursor.fetchone()
        if fine_amount[0]:
            return int(fine_amount[0])
        else:
            return 0
    except Exception as e:
        return "Error calculating fine"

@router.get("/pay_fine/{user_id}")
async def get_fine(request: Request, user_id):
    try:
        cursor = request.app.mysql.cursor()
        statement = "update issue set fine = 0 where user_id = '{}'".format(user_id)
        cursor.execute(statement)
        request.app.mysql.commit()
        return "Fine Cleared!"
    except Exception as e:
        return "Error calculating fine"