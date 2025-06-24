from datetime import datetime
from typing import Annotated, List

from sqlalchemy import and_
from sqlalchemy.orm import Session
from database import get_db
from models import Tickets

db = Annotated[Session, get_db]

class TicketRepository:
    def __init__(self, db):
        self.db = db

    # CRUD
    # 分析型方法
    def get_tickets_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Tickets]:
        """获取指定日期范围内的工单"""
        return self.db.query(Tickets).filter(
            and_(
                Tickets.reported_at >= start_date,
                Tickets.reported_at < end_date
            )
        ).all()
