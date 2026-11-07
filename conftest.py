"""Point d'entrée pytest : enregistre les fixtures du framework, rangées par thème."""

import pytest

from framework.config.settings import Settings

pytest_plugins = [
    "framework.fixtures.browser",
    "framework.fixtures.api",
    "framework.fixtures.auth",
    "framework.fixtures.data",
    "framework.fixtures.pages",
]


@pytest.fixture(scope="session")
def base_url(settings: Settings) -> str:
    """URL du site, issue de l'environnement choisi (ENV).

    Définie ici et non dans framework/fixtures : pytest-playwright enregistre sa propre
    fixture base_url après nos plugins, seul ce conftest racine est prioritaire sur elle.
    """
    return settings.base_url
