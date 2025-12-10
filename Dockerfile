FROM python:3.10

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Playwright 설치
RUN pip install playwright
RUN playwright install --with-deps

COPY . /app/

CMD ["pytest", "-s", "--disable-warnings"]
