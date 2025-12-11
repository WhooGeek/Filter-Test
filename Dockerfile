# 1) Python 3.11 기반 이미지
FROM python:3.11-slim

# 2) 작업 디렉토리
WORKDIR /app

# 3) 시스템 패키지 업데이트 & Playwright 브라우저 설치용 의존성 설치
RUN apt-get update && apt-get install -y \
    bash \
    curl \
    wget \
    git \
    libglib2.0-0 \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libxkbcommon0 \
    libatspi2.0-0 \
    libdrm2 \
    libgtk-3-0 \
    libasound2 \
    libcups2 \
    && rm -rf /var/lib/apt/lists/*

# 4) requirements.txt 복사
COPY requirements.txt .

# 5) Python 라이브러리 설치
RUN pip install --no-cache-dir -r requirements.txt

# 6) Playwright 및 브라우저 설치
RUN pip install playwright
RUN playwright install --with-deps

# 7) 프로젝트 전체 복사
COPY . .

# 8) 기본 실행 명령 (pytest 실행)
CMD ["pytest", "-s"]

# 9) 도커로 실행 시 웹 애플리케이션이 도커 환경임을 인지할 수 있도록 환경 변수 설정
ENV RUNNING_IN_DOCKER=true