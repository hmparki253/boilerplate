from concurrent.futures import ProcessPoolExecutor
import pandas as pd
from loguru import logger
from fastapi import Request

executor = ProcessPoolExecutor(max_workers=4)

def cpu_intensive_task():
    # 현재 컨텍스트의 trace_id를 사용하여 로깅
    logger.debug("Starting CPU intensive task")
    total = 0
    for i in range(10**8):
        total += i
    logger.info(f"CPU intensive task completed. Result: {total}")
    return total

async def heavy_data_processing(request: Request):
    # 미들웨어에서 설정한 trace_id 사용
    trace_id = getattr(request.state, 'trace_id', 'no-trace-id')
    
    with logger.contextualize(trace_id=trace_id):
        logger.debug("Starting heavy data processing")
        try:
            n = 10**6
            df = pd.DataFrame({
                "col1": range(1, n + 1),
                "col2": range(n, 2*n)
            })
            result = df.groupby("col1").sum()
            logger.info("Heavy data processing completed successfully")
            return result.to_dict()
        except Exception as e:
            logger.error(f"Error in heavy data processing: {str(e)}")
            raise 