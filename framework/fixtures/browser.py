"""Réglages du navigateur : surcharge des fixtures fournies par pytest-playwright."""

from typing import Any

import pytest
from playwright.sync_api import Playwright

from framework.config.settings import Settings, get_settings


@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_settings()


@pytest.fixture(scope="session", autouse=True)
def _test_id_attribute(playwright: Playwright) -> None:
    """get_by_test_id() cible l'attribut data-test utilisé par l'application."""
    playwright.selectors.set_test_id_attribute("data-test")


@pytest.fixture(scope="session")
def connect_options(settings: Settings) -> dict[str, Any] | None:
    """Avec PLAYWRIGHT_SERVER défini (CI), on se connecte au serveur Playwright distant."""
    if settings.playwright_server:
        return {"endpoint": settings.playwright_server}
    return None


@pytest.fixture(scope="session")
def browser_type_launch_args(
    browser_type_launch_args: dict[str, Any], pytestconfig: pytest.Config
) -> dict[str, Any]:
    """En mode --headed (local), la fenêtre s'ouvre en plein écran."""
    if pytestconfig.getoption("--headed"):
        return {**browser_type_launch_args, "args": ["--start-maximized"]}
    return browser_type_launch_args


@pytest.fixture(scope="session")
def browser_context_args(
    browser_context_args: dict[str, Any], pytestconfig: pytest.Config
) -> dict[str, Any]:
    args = {
        **browser_context_args,
        "locale": "fr-FR",
        "extra_http_headers": {"Accept-Language": "fr-FR,fr;q=0.9"},
    }
    if pytestconfig.getoption("--headed"):
        # La page occupe toute la fenêtre maximisée au lieu d'un viewport fixe
        args["no_viewport"] = True
    return args
