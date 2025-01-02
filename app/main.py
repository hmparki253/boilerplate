from fastapi import FastAPI
from concurrent.futures import ProcessPoolExecutor
import asyncio
import aiofiles
import pandas as pd
import time

app = FastAPI()
executor = ProcessPoolExecutor(max_workers=4)

@app.get("/blocking")
def blocking_endpoint():
    result = cpu_intensive_task()
    return {"result": result}

def cpu_intensive_task():
    total = 0
    for i in range(10**8):
        total += i
    return total

def heavy_data_processing():
    n = 10**6  # 동일한 길이
    df = pd.DataFrame({
        "col1": range(1, n + 1),
        "col2": range(n, 2*n)
    })
    result = df.groupby("col1").sum()
    return result.to_dict()

# 비동기적으로 결과를 파일에 기록
async def write_to_file(file_path: str, data: dict):
    async with aiofiles.open(file_path, mode='a') as f:
        # 행 단위로 파일에 기록
        for key, value in data.items():
            line = f"{key}: {value}\n"
            await f.write(line)

@app.get("/non-blocking")
async def nonblocking_endpoint():
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(executor, heavy_data_processing)

    # 결과를 파일로 저장
    file_path = "heavy_data_result.txt"
    await write_to_file(file_path, result)

    return {"status": "success", "file_path": file_path}