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
        self.email.press_sequentially(username, delay=200)
        
        # 'Tab' 키로 자연스러운 Blur 유도
        self.email.press("Tab") 
        self.page.wait_for_timeout(500)

        # 비밀번호 입력
        self.password.click()
        self.password.press_sequentially(password, delay=200)
        self.password.press("Tab") # 탭 눌러서 포커스 해제
        self.page.wait_for_timeout(1000)
        
        # 버튼 활성화 'Assertions' (Retry 로직 내장)
        # enabled 될 때까지 Playwright가 계속 찔러봅니다.
        expect(self.submit_btn).to_be_enabled(timeout=30000) # CI 고려 15초로 넉넉하게

        print("로그인 버튼 클릭 시도...")
        try:
            with self.page.expect_navigation(timeout=30000):
                self.submit_btn.click(force=True)
        except Exception as e:
            print(f"페이지 이동 감지 실패: {e}")

        # 로그인 성공 확인
        print("로그인 성공 여부 확인 중...")
        expect(self.user_avatar).to_be_visible(timeout=30000)