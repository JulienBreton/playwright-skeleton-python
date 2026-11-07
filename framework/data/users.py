"""Fabrique de données de test : des clients uniques pour isoler chaque test."""

from typing import Any
from uuid import uuid4

from framework.api.models import Address, NewUser

DEFAULT_PASSWORD = "Sk3leton!Pass#2026"


def build_new_user(**overrides: Any) -> NewUser:
    """Construit un client avec un email unique.

    Les champs passés en argument remplacent les valeurs par défaut.
    """
    values: dict[str, Any] = {
        "first_name": "Test",
        "last_name": "Skeleton",
        "dob": "1990-01-01",
        "phone": "0600000000",
        "address": Address(
            street="1 rue de Test", city="Paris", state="IDF", country="FR", postal_code="75001"
        ),
        "email": f"skeleton.{uuid4().hex[:12]}@example.com",
        "password": DEFAULT_PASSWORD,
    }
    values.update(overrides)
    return NewUser(**values)
