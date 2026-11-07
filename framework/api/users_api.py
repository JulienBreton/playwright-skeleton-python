from framework.api.base_client import BaseApiClient
from framework.api.models import NewUser, Token, User
from framework.config.settings import Credentials


class UsersApi(BaseApiClient):
    def register(self, user: NewUser) -> User:
        response = self.request.post("/users/register", data=user.model_dump())
        return User.model_validate(self.json(response, expected_status=201))

    def login(self, credentials: Credentials) -> str:
        response = self.request.post(
            "/users/login",
            data={"email": credentials.email, "password": credentials.password},
        )
        return Token.model_validate(self.json(response)).access_token

    def me(self, token: str) -> User:
        response = self.request.get("/users/me", headers=self.bearer(token))
        return User.model_validate(self.json(response))

    def delete(self, user_id: str, admin_token: str) -> None:
        response = self.request.delete(f"/users/{user_id}", headers=self.bearer(admin_token))
        self.check(response, expected_status=204)
