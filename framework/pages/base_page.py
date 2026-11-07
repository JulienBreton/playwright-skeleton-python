from typing import ClassVar, Self

from playwright.sync_api import Page

from framework.pages.components.header import Header


class BasePage:
    """Base de toutes les pages : chaque page déclare son chemin relatif (`path`)."""

    path: ClassVar[str] = ""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.header = Header(page)

    def open(self) -> Self:
        # Chemin relatif : la base_url vient de la configuration de l'environnement
        self.page.goto(f"/{self.path}")
        return self
