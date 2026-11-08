import pytest
from playwright.sync_api import expect

from framework.pages.account_page import AccountPage

pytestmark = pytest.mark.ui


@pytest.mark.smoke
def test_account_page_opens_with_saved_session(account_page: AccountPage) -> None:
    # Pas de connexion ici : la session client est injectée par tests/ui/customer/conftest.py
    account_page.open()

    expect(account_page.title).to_have_text("Mon compte")
