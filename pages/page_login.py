# pages/page_login.py
import time
from playwright.sync_api import Page, expect

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.email = page.locator("#email-inp")
        self.password = page.locator("#pwd_inp")
        self.submit_btn = page.locator("button#btn-signin")
        self.user_avatar = page.locator("a.user-avatar")  # 로그인 후 뜨는 요소

    def login(self, username: str, password: str):
        self.email.click()
        self.email.fill("")  # 입력 필드 초기화
        self.email.type(username, delay=50)  

        self.password.click()
        self.password.fill("")
        self.password.type(password, delay=50)

        # 버튼 비활성 예외 처리
        for _ in range(20):
            if self.submit_btn.is_enabled():
                break
            time.sleep(0.5)
        else:
            raise Exception("로그인 버튼이 활성화되지 않았습니다.")

        self.submit_btn.click()

        expect(self.user_avatar).to_be_visible(timeout=5000)   #로그인 성공 대기

