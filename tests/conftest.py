import pytest
import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# Page Objects import
from pages.page_main import MainPage
from pages.page_login import LoginPage

load_dotenv() # .env 파일 로드

# 1. 환경 변수 설정
EMAIL = os.getenv("FG_ID")
PASSWORD = os.getenv("FG_PW")

# 2. 실행 모드 감지 로직 (핵심 수정 부분)
# GitHub Actions는 자동으로 'CI=true'를 설정해줍니다.
IS_CI = os.getenv("CI", "false") == "true"
IS_DOCKER = os.getenv("RUNNING_IN_DOCKER", "false") == "true"

# CI 환경이거나 Docker 환경이면 Headless로 실행 (창을 띄우지 않음)
HEADLESS_MODE = IS_CI or IS_DOCKER

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
    print(f"\n[Browser Setup] Headless Mode: {HEADLESS_MODE}")
    # --- 디버깅용 로그 추가 ---
    print("\n" + "="*30)
    print(f"Checking Env Vars in CI:")
    
    id_val = os.getenv("FG_ID")
    pw_val = os.getenv("FG_PW")

    # 값이 있는지 없는지 O/X로 출력 (보안상 실제 값 출력 X)
    print(f" -> FG_ID Exists? : {'YES' if id_val else 'NO (Empty!)'}")
    print(f" -> FG_PW Exists? : {'YES' if pw_val else 'NO (Empty!)'}")
    print("="*30 + "\n")
    # -----------------------
    browser = playwright_instance.chromium.launch(
        headless=HEADLESS_MODE,  # ✅ 환경에 따라 True/False 자동 적용
        args=[
            "--disable-blink-features=AutomationControlled",
            "--disable-gpu",
            "--disable-dev-shm-usage",
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-web-security",
            "--disable-features=IsolateOrigins,site-per-process",
        ]
    )
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def page(browser):
    # 브라우저 컨텍스트 생성 (뷰포트 크기 등을 여기서 설정 가능)
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080} # CI 환경에서 화면 크기 고정 (권장)
    )
    page = context.new_page()
    yield page
    context.close()

@pytest.fixture
def main_page(page):
    return MainPage(page)

@pytest.fixture
def login_page(page):
    return LoginPage(page)