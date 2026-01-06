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
        self.page.wait_for_load_state("domcontentloaded") # 입력창 준비 완료 확인
        
        # 이메일 입력
        # locator.press_sequentially 사용 (요소에 직접 입력)
        # delay를 100ms로 늘려 CI의 낮은 CPU 성능을 고려
        self.email.click() # 클릭 유지
        self.email.press_sequentially(username, delay=100)
        
        # 'Tab' 키로 자연스러운 Blur 유도
        self.email.press("Tab") 
        self.page.wait_for_timeout(500)

        # 비밀번호 입력
        self.password.click()
        self.password.press_sequentially(password, delay=100)
        self.password.press("Tab") # 탭 눌러서 포커스 해제
        
        # 버튼 활성화 'Assertions' (Retry 로직 내장)
        # enabled 될 때까지 Playwright가 계속 찔러봅니다.
        expect(self.submit_btn).to_be_enabled(timeout=15000) # CI 고려 15초로 넉넉하게
        self.submit_btn.click()

        # 로그인 성공 확인
        expect(self.user_avatar).to_be_visible(timeout=10000)