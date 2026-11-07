import re

import pytest
from playwright.sync_api import Page, expect

from framework.config.settings import Credentials
from framework.fixtures.data import CreatedCustomer
from framework.pages.account_page import AccountPage
from framework.pages.login_page import LoginPage

pytestmark = pytest.mark.ui


@pytest.mark.smoke
def test_login_with_new_customer(
    login_page: LoginPage, account_page: AccountPage, new_customer: CreatedCustomer
) -> None:
    # new_customer : compte créé via l'API pour ce test, supprimé à la fin
    login_page.open()
    login_page.login(new_customer.credentials)

    account_page.wait_until_loaded()
    expect(account_page.title).to_have_text("Mon compte")
    expect(account_page.header.user_menu).to_contain_text(
        f"{new_customer.user.first_name} {new_customer.user.last_name}"
    )


def test_login_rejected_with_invalid_credentials(login_page: LoginPage, page: Page) -> None:
    login_page.open()

    # Compte inexistant : évite de bloquer un vrai compte après plusieurs échecs
    login_page.submit(Credentials("unknown.account@example.com", "wrong-password"))

    expect(login_page.error_message).to_have_text("Invalid email or password")
    expect(page).to_have_url(re.compile(r".*/auth/login"))
