from playwright.sync_api import Page


class ProductGrid:
    """Grille des produits affichés (accueil, résultats de recherche)."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.product_names = page.get_by_test_id("product-name")
        self.search_caption = page.get_by_test_id("search-caption")
