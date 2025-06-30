from datetime import date
from pydantic import BaseModel, ValidationError
from fastapi import APIRouter, Query, Depends, HTTPException, Path
from sqlalchemy.exc import SQLAlchemyError

from database import db_dependency
from models import Tickets
from repositories.tickets_crud import TicketRepository, TicketsRangeQuery, TicketsRangeQuery1, TicketsRangeQuery2, TicketsRangeAndEventType4Query
from 语法test import ai_main

router = APIRouter(
    prefix="/tickets",
    tags=["工单CRUD"],
)


# 获取单张ticket
@router.get("/get_ticket", status_code=200)
async def get_ticket(db: db_dependency, ticket_id: str = Query(..., description="工单ID")):
    try:
        dao = TicketRepository(db)
        ticket = dao.get_ticket_by_id(ticket_id)

        if not ticket:
            raise HTTPException(status_code=404, detail="工单不存在")
        return ticket

    except HTTPException:
        # 重新抛出HTTP异常
        raise
    except SQLAlchemyError as e:
        # 数据库相关错误
        raise HTTPException(status_code=500, detail="数据库操作失败")
    except Exception as e:
        # 其他未预期的错误
        raise HTTPException(status_code=500, detail="服务器内部错误")


# 删除单张ticket
@router.delete("/delete_ticket/{ticket_id}", status_code=200)
async def delete_ticket(db: db_dependency, ticket_id: str = Path(..., description="要删除的工单ID")):
    dao = TicketRepository(db)
    count = dao.delete_ticket_by_id(ticket_id)

    if not count:
        return {"success": False, "message": f"⚠️ 没有找到对应的 Ticket: {ticket_id}"}
    return {"success": True, "deleted": count, "message": f"✅ 成功删除 {count} 条记录"}


# 获取一段时间的tickets
@router.get("/get_tickets_by_range", status_code=200)
async def get_tickets_by_range(db: db_dependency, ticket_range: TicketsRangeQuery = Depends()):
    try:
        dao = TicketRepository(db)
        tickets = dao.get_tickets_by_date_range(ticket_range)
        return tickets

    except HTTPException:
        # 重新抛出HTTP异常（比如参数验证失败）
        raise
    except SQLAlchemyError as e:
        # 数据库相关错误
        raise HTTPException(status_code=500, detail="数据库查询失败")
    except ValidationError as e:
        # Pydantic验证错误（如果TicketsRangeQuery验证失败）
        raise HTTPException(status_code=422, detail=f"参数验证失败: {str(e)}")
    except Exception as e:
        # 其他未预期的错误
        raise HTTPException(status_code=500, detail="服务器内部错误")


# 获取两段时间的tickets，然后对比
@router.get("/get_tickets_of_two_weeks", status_code=200)
async def get_tickets_of_two_weeks(db: db_dependency, first_week: TicketsRangeQuery1 = Depends(),
                                   second_week: TicketsRangeQuery2 = Depends()):
    dao = TicketRepository(db)
    first = TicketsRangeQuery(start_date=first_week.start_date_1, end_date=first_week.end_date_1)
    second = TicketsRangeQuery(start_date=second_week.start_date_2, end_date=second_week.end_date_2)

    tickets1 = dao.get_tickets_by_date_range(first)
    tickets2 = dao.get_tickets_by_date_range(second)

    return {"first_period": tickets1.get("tickets data"),
            "first_count": tickets1.get("Count"),
            "second_period": tickets2.get("tickets data"),
            "second_count": tickets2.get("Count"),
            }

@router.get("/get_tickets_by_date_and_type3", status_code=200, summary="按 event_type_3 分组统计 event_type_4 的数")
async def get_tickets_by_date_and_type3(
        db: db_dependency,
        params: TicketsRangeAndEventType4Query = Depends(),
):
    dao = TicketRepository(db)
    result = dao.get_tickets_by_date_and_type(params)
    print(result)
    return result


@router.get("/get_tickets_by_type", status_code=200, summary="AI分析")
async def get_tickets_by_type(db: db_dependency, params: TicketsRangeAndEventType4Query = Depends()):
    dao = TicketRepository(db)
    result = dao.get_tickets_by_date_and_type(params)
    print(result)
    ai_response = ai_main(result)

    # return {"data": result, "event_type_3": params.event_type_3}

    return ai_response

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
