from copy import deepcopy
from typing import Any
from pydantic import BaseModel, computed_field


class CreatedUser(BaseModel):
    register_data: dict[str, str]
    response_data: dict[str, Any]

    @computed_field  # type: ignore
    @property
    def login_data(self) -> dict[str, str]:
        login_data = deepcopy(self.register_data)
        login_data.pop('name')
        return login_data

    @computed_field  # type: ignore
    @property
    def access_token(self) -> str:
        return self.response_data['accessToken']
