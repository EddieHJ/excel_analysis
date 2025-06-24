from database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from zoneinfo import ZoneInfo

# 时区设置
def beijing_now():
    return datetime.now(ZoneInfo("Asia/Shanghai"))


class Tickets(Base):
    __tablename__ = 'tickets'

    id = Column(String(64), primary_key=True, nullable=False, unique=True)
    title = Column(String(255))
    creator = Column(String(100))
    assignee = Column(String(100))
    urgency = Column(String(20))
    impact = Column(String(20))
    priority = Column(String(20))
    source = Column(String(100))
    reporter = Column(String(100))
    quantity = Column(Integer)
    jira_link = Column(String(255))
    org_1 = Column(String(100))
    org_2 = Column(String(100))
    org_3 = Column(String(100))
    event_type_1 = Column(String(100))
    event_type_2 = Column(String(100))
    event_type_3 = Column(String(100))
    event_type_4 = Column(String(100))
    reported_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    completed = Column(Boolean, default=False)
    escalated = Column(Boolean, default=False)
    lead_time = Column(String(50))









