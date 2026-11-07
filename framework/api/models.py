"""Modèles des données échangées avec l'API.

pydantic valide les réponses à l'exécution : si le format de l'API change,
le test échoue avec un message clair au lieu d'une erreur plus loin.
Seuls les champs utilisés par les tests sont déclarés ; les autres sont ignorés.
"""

from pydantic import BaseModel, ConfigDict


class ApiModel(BaseModel):
    model_config = ConfigDict(extra="ignore")


class Category(ApiModel):
    name: str


class Product(ApiModel):
    id: str
    name: str
    price: float
    category: Category


class ProductList(ApiModel):
    total: int
    data: list[Product]


class Address(ApiModel):
    street: str
    city: str
    state: str
    country: str
    postal_code: str


class NewUser(ApiModel):
    """Données envoyées pour créer un client."""

    first_name: str
    last_name: str
    dob: str
    phone: str
    address: Address
    email: str
    password: str


class User(ApiModel):
    id: str
    first_name: str
    last_name: str
    email: str


class Token(ApiModel):
    access_token: str
