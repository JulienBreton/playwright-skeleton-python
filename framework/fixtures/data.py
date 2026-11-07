"""Données de test isolées : chaque test crée ses données via l'API et les supprime ensuite."""

from collections.abc import Iterator
from dataclasses import dataclass

import pytest

from framework.api.models import User
from framework.api.users_api import UsersApi
from framework.config.settings import Credentials
from framework.data.users import build_new_user


@dataclass(frozen=True)
class CreatedCustomer:
    user: User
    credentials: Credentials


@pytest.fixture
def new_customer(users_api: UsersApi, admin_token: str) -> Iterator[CreatedCustomer]:
    """Client créé pour ce test uniquement, supprimé à la fin (même si le test échoue)."""
    new_user = build_new_user()
    user = users_api.register(new_user)
    yield CreatedCustomer(user, Credentials(new_user.email, new_user.password))
    users_api.delete(user.id, admin_token)
