from playwright.sync_api import Page

from framework.pages.base_page import BasePage
from framework.pages.components.product_grid import ProductGrid
from framework.pages.components.search_bar import SearchBar


class HomePage(BasePage):
    path = ""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.search_bar = SearchBar(page)
        self.grid = ProductGrid(page)
