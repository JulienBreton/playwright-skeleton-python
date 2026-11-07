import re

from playwright.sync_api import Page, expect

from framework.pages.base_page import BasePage


class AccountPage(BasePage):
    path = "account"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.title = page.get_by_test_id("page-title")

    def wait_until_loaded(self) -> None:
        # Synchronisation (et non vérification métier) : seule forme d'expect admise dans une page
        expect(self.page).to_have_url(re.compile(r".*/account"))
