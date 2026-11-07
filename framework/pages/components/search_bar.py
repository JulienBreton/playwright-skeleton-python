from urllib.parse import urlparse

from playwright.sync_api import Page, Response

from framework.api.models import ProductList


class SearchBar:
    """Champ de recherche de la barre latérale."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.query_input = page.get_by_test_id("search-query")
        self.submit_button = page.get_by_test_id("search-submit")

    def search(self, query: str) -> ProductList:
        """Lance la recherche et renvoie la réponse de l'API, qui sert de référence aux tests."""
        self.query_input.fill(query)
        # expect_response commence à écouter AVANT le clic, pour ne pas rater la réponse
        with self.page.expect_response(_is_search_response) as response_info:
            self.submit_button.click()
        return ProductList.model_validate(response_info.value.json())


def _is_search_response(response: Response) -> bool:
    return urlparse(response.url).path == "/products/search" and response.ok
