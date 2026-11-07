"""Sessions enregistrées (storage state) : connexion une seule fois par rôle et par worker.

Les dossiers tests/ui/<rôle>/conftest.py injectent la session correspondante dans le navigateur.
Ces comptes sont partagés : les tests qui modifient des données utilisent `new_customer`.
"""

from pathlib import Path
from typing import Any

import pytest
from playwright.sync_api import Browser

from framework.config.settings import ROOT_DIR, Credentials, Settings
from framework.pages.login_page import LoginPage

AUTH_DIR = ROOT_DIR / ".auth"


def _save_storage_state(
    browser: Browser, context_args: dict[str, Any], credentials: Credentials, file: Path
) -> str:
    context = browser.new_context(**context_args)
    try:
        login_page = LoginPage(context.new_page()).open()
        login_page.login(credentials)
        file.parent.mkdir(parents=True, exist_ok=True)
        context.storage_state(path=file)
    finally:
        context.close()
    return str(file)


@pytest.fixture(scope="session")
def customer_storage_state(
    browser: Browser, browser_context_args: dict[str, Any], settings: Settings, worker_id: str
) -> str:
    # worker_id (pytest-xdist) : un fichier par worker, pas de conflit en parallèle
    file = AUTH_DIR / f"customer-{worker_id}.json"
    return _save_storage_state(browser, browser_context_args, settings.customer, file)


@pytest.fixture(scope="session")
def admin_storage_state(
    browser: Browser, browser_context_args: dict[str, Any], settings: Settings, worker_id: str
) -> str:
    file = AUTH_DIR / f"admin-{worker_id}.json"
    return _save_storage_state(browser, browser_context_args, settings.admin, file)
