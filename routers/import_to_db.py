import logging

from fastapi import APIRouter
from typing import Annotated

import pandas as pd
from fastapi import Depends
from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
import models
from models import Tickets
from database import SessionLocal

router = APIRouter(
    prefix="/import_to_db",
    tags=["导入数据库"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def convert_yn_to_bool(value):
    if isinstance(value, str):
        return value.strip().upper() == 'Y'
    return False


@router.post("/import")
async def import_excel_to_db(db: db_dependency, file_path: str = "data/output.xlsx"):
    df = pd.read_excel(file_path)

    # Excel 列 → 数据库字段 映射（请按你实际列名调整）
    df.rename(columns={
        "任务ID": "id",
        "标题": "title",
        "创建者": "creator",
        "执行者": "assignee",
        "紧急程度": "urgency",
        "影响级": "impact",
        "优先级": "priority",
        "事件来源": "source",
        "联系人": "reporter",
        "单量": "quantity",
        "Jira工单": "jira_link",
        "组织1": "org_1",
        "组织2": "org_2",
        "事件类型1": "event_type_1",
        "事件类型2": "event_type_2",
        "事件类型3": "event_type_3",
        "事件类型4": "event_type_4",
        "报单时间": "reported_at",
        "完成时间": "completed_at",
        "是否完成": "completed",
        "借助伙伴资源": "escalated",
        "Lead Time": "lead_time",
    }, inplace=True)

    # 转换布尔字段
    df['completed'] = df['completed'].apply(convert_yn_to_bool)
    df['escalated'] = df['escalated'].apply(convert_yn_to_bool)

    # 强制将 NaT / NaN 转为 None（防止 'NaT' 字符串进入数据库）
    # 更彻底地将 NaT 转换为 None
    df['reported_at'] = df['reported_at'].astype(object).where(pd.notna(df['reported_at']), None)
    df['completed_at'] = df['completed_at'].astype(object).where(pd.notna(df['completed_at']), None)

    # 再给其他列填充空字符串，排除时间列
    time_columns = ["reported_at", "completed_at"]
    df.fillna(value={col: "" for col in df.columns if col not in time_columns}, inplace=True)

    for _, row in df.iterrows():
        ticket_data = row.to_dict()
        ticket = models.Tickets(**ticket_data)
        db.add(ticket)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()  # 回滚当前事务，避免阻塞后续插入
            logger.warning(f"⛔ 跳过重复主键 ID: {ticket.id}")


    return {"message": "✅ 数据导入完成", "rows": len(df)}
