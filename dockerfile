#베이스 이미지
FROM python:3.12-slim

#work dir 설정
WORKDIR /app

#의존성
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#앱 코드 복사
COPY . .

#포트
EXPOSE 8000

#앱 실행 커맨드
CMD ["uvicorn", "auth_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
