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
        self.page.wait_for_load_state("networkidle") # 네트워크 안정화 대기

        # 이메일 입력
        self.email.click()
        self.email.focus() # focus 명시적 호출
        self.page.keyboard.type(username, delay=80)

        self.email.evaluate("el => el.dispatchEvent(new Event('input', { bubbles: true}))")
        self.email.evaluate("el => el.dispatchEvent(new Event('change', { bubbles: true}))")
        self.page.wait_for_timeout(300)

        # 비밀번호 입력
        self.password.click()
        self.password.focus()
        self.page.keyboard.type(password, delay=80)

        self.password.evaluate("el => el.dispatchEvent(new Event('input', { bubbles : true }))")
        self.password.evaluate("el => el.dispatchEvent(new Event('change', { bubbles : true }))")
        self.page.wait_for_timeout(300)
        

        # 버튼 활성화 대기
        self.submit_btn.wait_for(state="enabled", timeout=10000)
        self.submit_btn.click()

        # 로그인 성공 요소 확인
        expect(self.user_avatar).to_be_visible(timeout=5000)