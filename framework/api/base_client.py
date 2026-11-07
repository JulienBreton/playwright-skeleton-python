from typing import Any

from playwright.sync_api import APIRequestContext, APIResponse


class ApiError(AssertionError):
    """Réponse HTTP inattendue. Hérite d'AssertionError pour apparaître comme un échec de test."""


class BaseApiClient:
    """Base des clients API : un client par ressource (produits, utilisateurs...)."""

    def __init__(self, request: APIRequestContext) -> None:
        self.request = request

    @staticmethod
    def bearer(token: str) -> dict[str, str]:
        return {"Authorization": f"Bearer {token}"}

    @staticmethod
    def check(response: APIResponse, expected_status: int) -> APIResponse:
        if response.status != expected_status:
            raise ApiError(
                f"{response.url} : statut {response.status} au lieu de {expected_status}\n"
                f"{response.text()[:500]}"
            )
        return response

    def json(self, response: APIResponse, expected_status: int = 200) -> Any:
        return self.check(response, expected_status).json()
