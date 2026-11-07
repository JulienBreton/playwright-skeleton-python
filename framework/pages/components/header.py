from playwright.sync_api import Page


class Header:
    """Barre de navigation, présente sur toutes les pages."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.sign_in_link = page.get_by_test_id("nav-sign-in")
        self.contact_link = page.get_by_test_id("nav-contact")
        self.user_menu = page.get_by_test_id("nav-menu")

    def go_to_sign_in(self) -> None:
        self.sign_in_link.click()
