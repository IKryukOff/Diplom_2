from typing import Generator
import pytest
from faker import Faker
from methods.user_methods import UserMethods


@pytest.fixture()
def user_data() -> dict[str, str]:
    fake = Faker()
    return {'email': fake.email(),
            'password': fake.password(),
            'name': fake.name()}


@pytest.fixture()
def create_user(user_data: dict[str, str]) -> Generator[tuple[dict[str, str], str], None, None]:
    _, response_data = UserMethods.register(user_data=user_data)
    access_token = response_data['accessToken']
    yield (user_data, access_token)
    UserMethods.delete(access_token=access_token)
