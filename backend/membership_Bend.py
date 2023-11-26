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



