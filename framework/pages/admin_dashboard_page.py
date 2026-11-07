from playwright.sync_api import Page

from framework.pages.base_page import BasePage


class AdminDashboardPage(BasePage):
    path = "admin/dashboard"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.title = page.get_by_test_id("page-title")
