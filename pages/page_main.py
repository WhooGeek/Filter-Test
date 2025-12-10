from playwright.sync_api import Page

class MainPage:
    def __init__(self, page):
        self.page = page
        self.url = "https://www.fashiongo.net/"

    def goto(self):
        self.page.goto(self.url)

    def click_login(self):
        self.page.click("#login-btn")
