# pages/page_login.py (수정 제안)
from playwright.sync_api import Page, expect, TimeoutError

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.email = page.locator("#email-inp")
        self.password = page.locator("#pwd_inp")
        self.submit_btn = page.locator("button#btn-signin")
        self.user_avatar = page.locator("a.user-avatar")

    def login(self, username: str, password: str):
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(500)  # 짧게 여유

        # 보일 때까지 기다리기
        expect(self.email).to_be_visible(timeout=5000)
        expect(self.password).to_be_visible(timeout=5000)

        # 더 안정적 입력 (fill은 기존값을 덮음)
        self.email.fill(username, timeout=5000)
        self.password.fill(password, timeout=5000)

        # 포커스 아웃/Tab으로 클라이언트 검증 트리거
        try:
            self.password.press("Tab")
        except Exception:
            # 가끔 press가 실패하면 페이지 레벨로 Tab
            self.page.keyboard.press("Tab")

        # 버튼이 활성화될 때까지 대기 (최대 20초)
        try:
            expect(self.submit_btn).to_be_enabled(timeout=20000)
        except TimeoutError:
            # 디버깅 정보 수집
            self.page.screenshot(path="button_not_enabled.png")
            print("Email value:", self.email.input_value())
            # password는 보안상 출력하지 않는 것을 권장. 대신 길이만 출력:
            pwd_val = self.password.input_value()
            print("Password length:", len(pwd_val) if pwd_val is not None else "None")
            print("Submit disabled attribute:", self.submit_btn.get_attribute("disabled"))
            raise TimeoutError("로그인 버튼이 활성화되지 않았습니다.")

        # 클릭 및 네비게이션
        with self.page.expect_navigation(wait_until="domcontentloaded", timeout=60000):
            self.submit_btn.click()

        expect(self.user_avatar).to_be_visible(timeout=5000)