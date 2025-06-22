from fastapi import APIRouter
from starlette.status import HTTP_204_NO_CONTENT

import excel_processor

router = APIRouter(
    prefix="/convert",
    tags=["转换原数据"],
)

input_path = 'data/2025.xlsx'
output_path = 'data/output.xlsx'

@router.post("/convert_excel")
async def convert_endpoint():
    try:
        excel_processor.convert_raw_to_output(input_path, output_path)
        return {"msg": "转换成功", "output": output_path}

    except Exception as e:
        return {"msg": "转换失败", "error": str(e)}