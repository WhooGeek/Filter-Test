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

        try:
            cookie_button = self.page.locator('#onetrust-accept-btn-handler')
            if cookie_button.is_visible():
                cookie_button.click()
        except:
            pass
        
        self.page.wait_for_timeout(500)

        self.email.click()
        self.email.type(username, delay=50)
        self.page.wait_for_timeout(200)

        self.password.click()
        self.password.type(password, delay=50)
        self.page.wait_for_timeout(200)

        # 버튼 비활성 예외 처리
        for _ in range(40):
            if self.submit_btn.is_enabled():
                break
            time.sleep(0.5)
        else:
            raise Exception("로그인 버튼이 활성화되지 않았습니다.")

        self.submit_btn.click()

        # 로그인 성공 여부 확인
        expect(self.user_avatar).to_be_visible(timeout=5000)