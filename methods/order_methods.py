from typing import Any

import requests
from data.api_entrypoints import Entrypoints
from data.utils import get_status_code_and_data


class OrderMethods:
    @staticmethod
    def create_order(ingredients: list[str] = [],
                     access_token: str | None = None) -> tuple[int, dict[str, Any] | str]:
        response = requests.post(url=Entrypoints.orders,
                                 data={'ingredients': ingredients},
                                 headers={'Authorization': access_token} if access_token else None)
        return get_status_code_and_data(response)

    @staticmethod
    def get_orders(access_token: str | None = None) -> tuple[int, dict[str, Any] | str]:
        response = requests.get(url=Entrypoints.orders,
                                headers={'Authorization': access_token} if access_token else None)
        return get_status_code_and_data(response)
