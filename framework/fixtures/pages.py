"""Page objects injectés dans les tests : pas d'instanciation manuelle dans les tests."""

import pytest
from playwright.sync_api import Page

from framework.pages.account_page import AccountPage
from framework.pages.admin_dashboard_page import AdminDashboardPage
from framework.pages.home_page import HomePage
from framework.pages.login_page import LoginPage


@pytest.fixture
def home_page(page: Page) -> HomePage:
    return HomePage(page)


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture
def account_page(page: Page) -> AccountPage:
    return AccountPage(page)


@pytest.fixture
def admin_dashboard_page(page: Page) -> AdminDashboardPage:
    return AdminDashboardPage(page)
