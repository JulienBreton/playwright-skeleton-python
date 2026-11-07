"""Clients API, disponibles pour les tests d'API comme pour préparer les données des tests UI."""

from collections.abc import Iterator

import pytest
from playwright.sync_api import APIRequestContext, Playwright

from framework.api.products_api import ProductsApi
from framework.api.users_api import UsersApi
from framework.config.settings import Settings


@pytest.fixture(scope="session")
def api_request(playwright: Playwright, settings: Settings) -> Iterator[APIRequestContext]:
    context = playwright.request.new_context(base_url=settings.api_url)
    yield context
    context.dispose()


@pytest.fixture(scope="session")
def products_api(api_request: APIRequestContext) -> ProductsApi:
    return ProductsApi(api_request)


@pytest.fixture(scope="session")
def users_api(api_request: APIRequestContext) -> UsersApi:
    return UsersApi(api_request)


@pytest.fixture(scope="session")
def admin_token(users_api: UsersApi, settings: Settings) -> str:
    return users_api.login(settings.admin)
