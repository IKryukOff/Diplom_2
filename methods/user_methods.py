from typing import Any

import requests
from data.api_entrypoints import Entrypoints


class UserMethods:
    @staticmethod
    def register(user_data: dict[str, str]) -> tuple[int, dict[str, Any]]:
        response = requests.post(url=Entrypoints.register,
                                 data=user_data)
        return response.status_code, response.json()

    @staticmethod
    def delete(access_token: str) -> tuple[int, dict[str, Any]]:
        response = requests.delete(url=Entrypoints.user,
                                   headers={'Authorization': access_token})
        return response.status_code, response.json()

    @staticmethod
    def login(user_data: dict[str, str]) -> tuple[int, dict[str, Any]]:
        response = requests.post(url=Entrypoints.login,
                                 data=user_data)
        return response.status_code, response.json()

    @staticmethod
    def update(update_data: dict[str, str],
               access_token: str | None = None) -> tuple[int, dict[str, Any]]:
        response = requests.patch(
            url=Entrypoints.user,
            data=update_data,
            headers={'Authorization': access_token} if access_token else None)
        return response.status_code, response.json()
