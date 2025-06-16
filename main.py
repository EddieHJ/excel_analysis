# app/main.py
from fastapi import FastAPI
from database import engine
import models
from routers import convert, import_to_db

app = FastAPI()

# 初始化数据库表
models.Base.metadata.create_all(bind=engine)

app.include_router(convert.router)
app.include_router(import_to_db.router)


