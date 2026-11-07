import pytest

from framework.api.products_api import ProductsApi

pytestmark = pytest.mark.api


@pytest.mark.smoke
def test_search_returns_only_matching_products(products_api: ProductsApi) -> None:
    results = products_api.search("Pliers")

    assert results.data, "aucun produit renvoyé"
    assert results.total >= len(results.data)
    for product in results.data:
        assert "pliers" in product.name.lower(), product.name


def test_search_without_match_returns_empty_list(products_api: ProductsApi) -> None:
    results = products_api.search("produit-qui-n-existe-pas")

    assert results.total == 0
    assert results.data == []
