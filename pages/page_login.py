# pages/page_login.py
import time
from playwright.sync_api import Page, expect

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.email = page.locator("#email-inp")
        self.password = page.locator("#pwd_inp")
        self.submit_btn = page.locator("button#btn-signin")
        self.user_avatar = page.locator("a.user-avatar")

    def login(self, username: str, password: str):
        # 1. 네트워크 아이들 제거 -> 대신 요소가 'Editable' 상태인지 확인
        # domcontentloaded는 유지하되, 핵심은 입력창이 준비되었느냐입니다.
        self.page.wait_for_load_state("domcontentloaded")
        
        # [핵심 1] 이메일 입력
        # page.keyboard 대신 locator.press_sequentially 사용 (요소에 직접 입력)
        # delay를 100ms로 늘려 CI의 낮은 CPU 성능을 배려
        self.email.click() # 혹시 모를 포커스 트리거를 위해 클릭은 유지
        self.email.press_sequentially(username, delay=100)
        
        # [핵심 2] 'Tab' 키로 자연스러운 Blur 유도 (가장 확실한 유효성 검사 트리거)
        # 강제 dispatchEvent보다 Tab키가 프론트엔드 프레임워크 입장에서 더 자연스럽습니다.
        self.email.press("Tab") 
        
        # CI 속도 고려하여 아주 짧은 안정화 대기 (필수는 아니나 안전장치)
        self.page.wait_for_timeout(500)

        # [핵심 3] 비밀번호 입력
        self.password.click()
        self.password.press_sequentially(password, delay=100)
        self.password.press("Tab") # 입력 후 탭을 눌러 포커스 뺌 -> 유효성 검사 발동
        
        # [핵심 4] 버튼 활성화 'Assertions' (Retry 로직 내장)
        # 단순히 기다리는게 아니라, enabled 될 때까지 Playwright가 계속 찔러봅니다.
        expect(self.submit_btn).to_be_enabled(timeout=15000) # CI 고려 15초로 넉넉하게
        self.submit_btn.click()

        # 로그인 성공 확인
        expect(self.user_avatar).to_be_visible(timeout=10000)