from fastapi import APIRouter
import asyncio
from loguru import logger
from app.services.data_processing import cpu_intensive_task, heavy_data_processing, executor
import aiofiles
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime

processingRouter = APIRouter(
    prefix="/api/v1",
    tags=["processing"]
)

executor = ProcessPoolExecutor()

# heavy_data_processing을 동기 함수로 변경
def heavy_data_processing():
    # 딕셔너리 형태로 반환하도록 수정
    return {"status": "처리 완료", "timestamp": str(datetime.now())}

@processingRouter.get("/blocking")
async def blocking_endpoint():
    logger.info("Handling blocking request")
    result = cpu_intensive_task()
    return {"result": result}

@processingRouter.get("/non-blocking")
async def nonblocking_endpoint():
    logger.info("Handling non-blocking request")
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(executor, heavy_data_processing)

    # 결과를 파일로 저장
    file_path = "heavy_data_result.txt"
    async with aiofiles.open(file_path, mode='a') as f:
        for key, value in result.items():  # 이제 딕셔너리의 items() 메소드 사용 가능
            line = f"{key}: {value}\n"
            await f.write(line)
            
    logger.info(f"Results saved to {file_path}")
    return {"status": "success", "file_path": file_path} 