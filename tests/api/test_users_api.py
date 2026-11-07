import pytest

from framework.api.users_api import UsersApi
from framework.fixtures.data import CreatedCustomer

pytestmark = pytest.mark.api


def test_new_customer_can_log_in_and_read_profile(
    users_api: UsersApi, new_customer: CreatedCustomer
) -> None:
    token = users_api.login(new_customer.credentials)
    profile = users_api.me(token)

    assert profile.id == new_customer.user.id
    assert profile.email == new_customer.credentials.email
