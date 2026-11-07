from playwright.sync_api import Page

from framework.config.settings import Credentials
from framework.pages.base_page import BasePage


class LoginPage(BasePage):
    path = "auth/login"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.email_input = page.get_by_test_id("email")
        self.password_input = page.get_by_test_id("password")
        self.submit_button = page.get_by_test_id("login-submit")
        self.error_message = page.get_by_test_id("login-error")

    def submit(self, credentials: Credentials) -> None:
        """Remplit et soumet le formulaire, sans présumer du résultat (cas d'échec)."""
        self.email_input.fill(credentials.email)
        self.password_input.fill(credentials.password)
        self.submit_button.click()

    def login(self, credentials: Credentials) -> None:
        """Se connecte et attend la réponse réussie de l'API d'authentification."""
        with self.page.expect_response(
            lambda response: "/users/login" in response.url and response.ok
        ):
            self.submit(credentials)
