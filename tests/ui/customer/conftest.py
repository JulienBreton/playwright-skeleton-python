from typing import Any

import pytest


@pytest.fixture(scope="session")
def browser_context_args(
    browser_context_args: dict[str, Any], customer_storage_state: str
) -> dict[str, Any]:
    """Tous les tests de ce dossier démarrent avec la session du client déjà ouverte."""
    return {**browser_context_args, "storage_state": customer_storage_state}
