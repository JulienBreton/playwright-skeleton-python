import re

import pytest
from playwright.sync_api import expect

from framework.pages.home_page import HomePage

pytestmark = pytest.mark.ui


@pytest.mark.parametrize(
    "query",
    [pytest.param("Pliers", marks=pytest.mark.smoke), "Hammer"],
)
def test_search_shows_matching_products(home_page: HomePage, query: str) -> None:
    home_page.open()

    # La réponse de l'API sert de référence : pas de nombre de produits codé en dur
    results = home_page.search_bar.search(query)

    expect(home_page.grid.search_caption).to_have_text(f"Searched for: {query}")
    assert results.data, f"aucun produit renvoyé pour « {query} »"
    expect(home_page.grid.product_names).to_have_text([product.name for product in results.data])
    expect(home_page.grid.product_names).to_have_text(
        [re.compile(query, re.IGNORECASE)] * len(results.data)
    )
