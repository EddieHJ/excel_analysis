import sys
from typing import Annotated

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from fastapi import Request, Depends

import time
import logging

# 连接配置
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Abc12345@localhost/data_ana"  # 连接PostgreSQL
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:Abc12345@127.0.1.1:3306/bjpowernode"  # 连接MySQL
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})  # Only for Sqlite
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 日志初始化（你也可以配置为写文件）

logger = logging.getLogger("sqlalchemy")
logging.basicConfig(level=logging.INFO)


def get_db():
    db = SessionLocal()
    start_time = time.perf_counter()
    try:
        yield db
    finally:
        db.close()
        duration = (time.perf_counter() - start_time) * 1000  # 转为毫秒
        logger.info(f"🗃️ DB session finished in {duration:.2f} ms")

db_dependency = Annotated[Session, Depends(get_db)]