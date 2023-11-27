from fastapi import FastAPI, Body
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware

import uvicorn


from users_Bend import router as users_router
from books_Bend import router as books_router
from membership_Bend import router as membership_router
from fine_Bend import router as fine_router

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'])



@app.on_event("startup")
async def startup_event():
    app.mysql = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysql12",
    database="lms"
)

    app.mysql.autocommit = True

@app.on_event("shutdown")
async def shutdown_event():
    app.mysql.close()

app.include_router(users_router, tags=['users'])
app.include_router(books_router, tags=['books'])
app.include_router(membership_router, tags=['membership'])
app.include_router(fine_router,tags=['fine'])

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)