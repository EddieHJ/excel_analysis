from datetime import date
from pydantic import BaseModel
from fastapi import APIRouter, Query, Depends
from database import db_dependency
from models import Tickets

router = APIRouter(
    prefix="/tickets",
    tags=["工单分析"],
)

class DateRangeQuery(BaseModel):
    start_date: date
    end_date: date

# class TicketIdQuery(BaseModel):
#     ticket_id: str

@router.get("/get_ticket", status_code=200)
async def get_ticket(db: db_dependency, ticket_id: str = Query(..., description="工单ID")):
    return db.query(Tickets).filter(
        Tickets.id == ticket_id,
    ).first()


@router.get("/get_tickets_by_range", status_code=200)
async def get_tickets_by_range(db: db_dependency, params: DateRangeQuery = Depends()):  # 可以用params = Annatated[DateRangeQuery, Depends()]，一样的意思，但是更繁琐。
    return db.query(Tickets).filter(
        Tickets.reported_at >= params.start_date,
        Tickets.reported_at <= params.end_date,
    ).all()

class TicketTypeQuery(BaseModel):
    type1: str
    type2: str


"""
一、这么写错误，因为用了BaseModel，这个params就是请求体，而Get是没有请求体的。
class TicketIdQuery(BaseModel):
    ticket_id: str
    
@router.get("/get_ticket", status_code=200)
async def get_ticket(db: db_dependency, params: TicketIdQuery=Depends()):

二、这么写错误，因为还是那个原因，get没有请求体
class TicketIdQuery(BaseModel):
    ticket_id: str
    
@router.get("/get_ticket", status_code=200)
async def get_ticket(db: db_dependency, params: TicketIdQuery):

"""

"""
题目1
编写一个 GET 接口 /search_items，接收两个查询参数：category（字符串）和 max_price（浮点数），返回一个字典包含接收到的参数。

用 Pydantic 模型封装参数并通过 Depends 注入。

说明请求时 URL 的示例。
"""
