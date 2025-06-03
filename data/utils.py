from typing import Any

from requests import JSONDecodeError, Response


def get_status_code_and_data(response: Response) -> tuple[int, dict[str, Any] | str]:
    try:
        return response.status_code, response.json()
    except JSONDecodeError:
        return response.status_code, response.text
