import pytest
from pages.page_main import MainPage
from pages.page_login import LoginPage
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os

load_dotenv() # env 파일 로드

EMAIL = os.getenv("FG_ID")
PASSWORD = os.getenv("FG_PW")
IS_DOCKER = os.getenv("RUNNING_IN_DOCKER", "false") == "true"

@pytest.fixture(scope="session")
def credentials():
    return {
        "email": EMAIL,
        "password": PASSWORD
    }

@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def browser(playwright_instance):
    browser = playwright_instance.chromium.launch(
        headless=IS_DOCKER,
        args=["--disable-blink-features=AutomationControlled", "--disable-gpu",
              '--disable-dev-shm-usage',      # ✅ /dev/shm 사용 안 함
                '--no-sandbox',                  # ✅ sandbox 비활성화
                '--disable-setuid-sandbox',      # ✅ setuid sandbox 비활성화
                '--disable-gpu',                 # ✅ GPU 비활성화
                '--disable-web-security',        # ✅ CORS 등 보안 정책 완화
                '--disable-features=IsolateOrigins,site-per-process',  # ✅ 프로세스 격리 비활성화
        ]
                
        )
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()

@pytest.fixture
def main_page(page):
    return MainPage(page)

@pytest.fixture
def login_page(page):
    return LoginPage(page)

