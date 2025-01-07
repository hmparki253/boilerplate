from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import uuid
from loguru import logger
import sys
import time
from datetime import datetime

# 로거 설정
logger.remove()
logger.add(
    "logs/api_{time:YYYY-MM-DD}.log",
    rotation="00:00",  # 매일 자정에 새로운 파일
    retention="30 days",  # 30일간 보관
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {extra[trace_id]} | {message}",
    enqueue=True,
    backtrace=True,
    diagnose=True
)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        trace_id = str(uuid.uuid4())
        
        # request.state에 trace_id 저장
        request.state.trace_id = trace_id
        
        with logger.contextualize(trace_id=trace_id):
            # 요청 정보 로깅
            start_time = time.time()
            logger.info(f"Request started: {request.method} {request.url}")
            logger.debug(f"Request headers: {request.headers}")
            
            try:
                # 요청 처리
                response = await call_next(request)
                
                # 처리 시간 계산
                process_time = time.time() - start_time
                
                # 응답 정보 로깅
                logger.info(
                    f"Request completed: {request.method} {request.url} "
                    f"- Status: {response.status_code} "
                    f"- Duration: {process_time:.3f}s"
                )
                
                # trace_id를 응답 헤더에 추가
                response.headers["X-Trace-ID"] = trace_id
                response.headers["X-Process-Time"] = str(process_time)
                
                return response
                
            except Exception as e:
                logger.error(f"Request failed: {str(e)}")
                raise
