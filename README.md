# FastAPI Boilerplate Code Repository

## Description
FastAPI 개발을 위한 사전 튜토리얼 및 코드 꾸러미 준비

## Setup Instructions
1. venv 생성 및 활성화
    ```shell
    cd boilerplate
    python -m venv venv
    source venv/bin/activate # Windows: venv\Scripts\activate
    ```
2. 의존성 설치
    ```shell
    pip install -r requirements.txt
    ```

3. 애플리케이션 실행
    ```shell
    cd /app # Windows: cd .\app\
    uvicorn main:app --reload # Single Process, auto reload enabled
    uvicorn main:app --reload --workers 4 # Four processes, auto reload enabled
    ```