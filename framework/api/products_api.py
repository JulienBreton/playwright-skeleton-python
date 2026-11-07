from framework.api.base_client import BaseApiClient
from framework.api.models import ProductList


class ProductsApi(BaseApiClient):
    def search(self, query: str) -> ProductList:
        response = self.request.get("/products/search", params={"q": query})
        return ProductList.model_validate(self.json(response))
