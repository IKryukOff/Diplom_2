from typing import Any

import requests
from data.api_entrypoints import Entrypoints
from data.utils import get_status_code_and_data


class UserMethods:
    @staticmethod
    def register(user_data: dict[str, str]) -> tuple[int, dict[str, Any] | str]:
        response = requests.post(url=Entrypoints.register,
                                 data=user_data)
        return get_status_code_and_data(response)

    @staticmethod
    def delete(access_token: str) -> tuple[int, dict[str, Any] | str]:
        response = requests.delete(url=Entrypoints.user,
                                   headers={'Authorization': access_token})
        return get_status_code_and_data(response)

    @staticmethod
    def login(user_data: dict[str, str]) -> tuple[int, dict[str, Any] | str]:
        response = requests.post(url=Entrypoints.login,
                                 data=user_data)
        return get_status_code_and_data(response)

    @staticmethod
    def update(update_data: dict[str, str],
               access_token: str | None = None) -> tuple[int, dict[str, Any] | str]:
        response = requests.patch(
            url=Entrypoints.user,
            data=update_data,
            headers={'Authorization': access_token} if access_token else None)
        return get_status_code_and_data(response)
