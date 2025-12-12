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
        self.page.wait_for_load_state("domcontentloaded")

        # 이메일 입력
        self.email.click()
        self.page.keyboard.type(username, delay=80)  # 실제 키보드 입력 느낌
        self.page.wait_for_timeout(200)
        self.email.blur()
        self.page.wait_for_timeout(200)

        # 비밀번호 입력
        self.password.click()
        self.page.keyboard.type(password, delay=80)
        self.page.wait_for_timeout(200)
        self.password.blur()
        self.page.wait_for_timeout(200)

        # 버튼 활성화 대기
        for _ in range(40):
            if self.submit_btn.is_enabled():
                break
            self.page.wait_for_timeout(300)
        else:
            raise Exception("로그인 버튼이 활성화되지 않았습니다.")

        self.submit_btn.click()

        # 로그인 성공 요소 확인
        expect(self.user_avatar).to_be_visible(timeout=5000)