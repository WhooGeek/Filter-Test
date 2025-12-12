# pages/page_login.py
from playwright.sync_api import Page, expect

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.email = page.locator("#email-inp")
        self.password = page.locator("#pwd_inp")
        self.submit_btn = page.locator("button#btn-signin")
        self.user_avatar = page.locator("a.user-avatar")

    def login(self, username: str, password: str):
        # 페이지 완전 로드 대기
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_load_state("networkidle")  # 네트워크까지 완전 대기
        self.page.wait_for_timeout(1500)  # 추가 여유
        
        # 입력 필드가 실제로 보일 때까지 대기
        self.email.wait_for(state="visible", timeout=5000)
        self.password.wait_for(state="visible", timeout=5000)

        # 이메일 입력
        self.email.click()
        self.email.type(username, delay=50)
        self.page.wait_for_timeout(500)

        # 비밀번호 입력
        self.password.click()
        self.password.type(password, delay=50)
        self.page.wait_for_timeout(500)

        # 버튼 활성화 폴링 (더 긴 timeout)
        max_attempts = 50
        for i in range(max_attempts):
            if not self.submit_btn.is_disabled():
                print(f"✅ 버튼 활성화됨 (시도 {i+1}/{max_attempts})")
                break
            self.page.wait_for_timeout(300)
        else:
            # 디버깅용 스크린샷
            self.page.screenshot(path="button_not_enabled.png")
            
            # 버튼 상태 확인
            is_disabled = self.submit_btn.get_attribute("disabled")
            print(f"❌ 버튼 disabled 속성: {is_disabled}")
            
            raise TimeoutError("로그인 버튼이 활성화되지 않았습니다.")

        # 로그인 버튼 클릭
        with self.page.expect_navigation(wait_until="domcontentloaded", timeout=60000):
            self.submit_btn.click()

        self.page.wait_for_timeout(1000)
        
        # 로그인 성공 확인
        expect(self.user_avatar).to_be_visible(timeout=5000)
        print("✅ 로그인 성공")