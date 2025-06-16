from database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from zoneinfo import ZoneInfo

# 时区设置
def beijing_now():
    return datetime.now(ZoneInfo("Asia/Shanghai"))


class Tickets(Base):
    __tablename__ = 'tickets'

    id = Column(String, primary_key=True, nullable=False, unique=True)
    title = Column(String)
    creator = Column(String)
    assignee = Column(String)
    urgency = Column(String)
    impact = Column(String)
    priority = Column(String)
    source = Column(String)
    reporter = Column(String)
    quantity = Column(Integer)
    jira_link = Column(String)
    org_1 = Column(String)
    org_2 = Column(String)
    org_3 = Column(String)
    event_type_1 = Column(String)
    event_type_2 = Column(String)
    event_type_3 = Column(String)
    event_type_4 = Column(String)
    reported_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    completed = Column(Boolean, default=False)
    escalated = Column(Boolean, default=False)
    lead_time = Column(String)









