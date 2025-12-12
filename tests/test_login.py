import os

def test_login(main_page, login_page, credentials):

    # main 으로 이동
    main_page.goto()

    # 로그인 페이지로 이동
    main_page.click_login()

    print("CI FG_ID", os.getenv("FG_ID"))
    print("CI FG_PW", os.getenv("FG_PW"))

    # 로그인 시도
    login_page.login(credentials["email"], credentials["password"])
    
    assert login_page.page.locator("a.user-avatar").is_visible()

   