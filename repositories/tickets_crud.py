# repositories/tickets_crud.py

from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import and_, select, delete, func, desc
from sqlalchemy.orm import Session
from database import db_dependency
from models import Tickets


# Pydantic模型
class TicketsRangeQuery(BaseModel):
    start_date: datetime
    end_date: datetime

class TicketsRangeQuery1(BaseModel):
    start_date_1: datetime
    end_date_1: datetime

class TicketsRangeQuery2(BaseModel):
    start_date_2: datetime
    end_date_2: datetime

class TicketsRangeAndEventType4Query(BaseModel):
    start_date: datetime
    end_date: datetime
    event_type_3: str

class TicketsRangeAndEventType4Query1(BaseModel):
    start_date_1: datetime
    end_date_1: datetime
    event_type_3_first: str

class TicketsRangeAndEventType4Query2(BaseModel):
    start_date_2: datetime
    end_date_2: datetime
    event_type_3_second: str


class TicketRepository:
    def __init__(self, db: db_dependency):
        self.db = db

    # CRUD
    # 分析型方法
    """获取两个日期段 + 特定event_type_3内的工单"""
    # def get_tickets_by_two_dates_and_type(self, date1: TicketsRangeQuery1, date2: TicketsRangeQuery2, event_type: str):



    """获取指定日期范围 + 特定event_type_3内的工单"""
    def get_tickets_by_date_and_type(self, params: TicketsRangeAndEventType4Query):
        stmt = (
            select(Tickets.event_type_4, func.count().label("count"))
            .where(
                Tickets.event_type_3 == params.event_type_3,
                Tickets.reported_at >= params.start_date,
                Tickets.reported_at <= params.end_date,
            )
            .group_by(Tickets.event_type_4)
            .order_by(desc("count"))
        )

        rows = self.db.execute(stmt).all()
        return [{"event_type_4": row[0], "count": row[1]} for row in rows]


    def get_tickets_by_date_range(self, params: TicketsRangeQuery):
        """获取指定日期范围内的工单"""
        stmt = select(Tickets).where(
            and_(
                Tickets.reported_at >= params.start_date,
                Tickets.reported_at < params.end_date,
            )
        ).order_by(Tickets.reported_at)

        tickets = self.db.execute(stmt).scalars().all()

        return {
            "tickets data": tickets,
            "Count": len(tickets)
        }

    # 获取ticket by id
    def get_ticket_by_id(self, ticket_id: str):
        stmt = select(Tickets).where(Tickets.id == ticket_id)
        return self.db.execute(stmt).scalars().one_or_none()


    # Delete ticket by id
    def delete_ticket_by_id(self, ticket_id: str):
        stmt = delete(Tickets).where(Tickets.id == ticket_id)
        result = self.db.execute(stmt)
        self.db.commit()
        return result.rowcount









