from fastapi import FastAPI
from app.middleware.logging import LoggingMiddleware
from app.router.processing import processingRouter
import aiofiles

app = FastAPI(
    title="Data Processing API",
    description="API for handling CPU intensive tasks",
    version="1.0.0"
)

# 미들웨어 추가
app.add_middleware(LoggingMiddleware)

# 라우터 등록
app.include_router(processingRouter)

# 헬스체크 엔드포인트
@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "healthy"}