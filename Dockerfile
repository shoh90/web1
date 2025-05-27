# Python 3.9 기반 이미지 사용
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 업데이트 및 필요한 패키지 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 파일 복사
COPY requirements.txt .

# Python 패키지 설치
RUN pip3 install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 포트 8501 노출 (Streamlit 기본 포트)
EXPOSE 8501

# Streamlit 설정
RUN mkdir -p ~/.streamlit/
RUN echo "\
[general]\n\
email = \"admin@company.com\"\n\
" > ~/.streamlit/credentials.toml

RUN echo "\
[server]\n\
headless = true\n\
enableCORS = false\n\
port = 8501\n\
" > ~/.streamlit/config.toml

# 헬스체크 추가
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# 애플리케이션 실행
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
