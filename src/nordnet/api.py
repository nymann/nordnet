from __future__ import annotations

import functools
from typing import Any, Callable

import requests

from nordnet.models.accounts import Account
from nordnet.models.accounts import AccountsResponse
from nordnet.models.accounts_info import AccountInfo
from nordnet.models.accounts_info import AccountsInfoResponse
from nordnet.session_handler import LoginSessionHandler
from nordnet.session_handler import SessionHandler
from nordnet.session_handler import UnauthenticatedSessionHandler


def ensure_authenticated(method: Callable) -> Callable:
    @functools.wraps(method)
    def wrapper(api: NordnetApi, *args: Any, **kwargs: Any) -> Any:
        if not api.session_handler.is_authenticated():
            api.session_handler.login()
            return wrapper(api, *args, **kwargs)
        return method(api, *args, **kwargs)

    return wrapper


class NordnetApi:
    def __init__(self) -> None:
        self.session = requests.Session()
        self._base_url = "https://www.nordnet.dk"
        self.session_handler: SessionHandler = UnauthenticatedSessionHandler(self.session)

    def login(self, username: str, password: str) -> dict:
        self.session_handler = LoginSessionHandler(
            session=self.session,
            username=username,
            password=password,
        )
        return self.session_handler.login()

    @ensure_authenticated
    def accounts(self) -> list[Account]:
        accounts_response = self.session.get(
            f"{self._base_url}/api/2/accounts",
            headers=self.session_handler.json_headers,
        )
        accounts_response.raise_for_status()
        return AccountsResponse.parse_obj(accounts_response.json()).__root__

    @ensure_authenticated
    def accounts_info(self, accounts: list[Account]) -> list[AccountInfo]:
        ids = ",".join(str(acc.accid) for acc in accounts)
        account_info_response = self.session.get(
            f"{self._base_url}/api/2/accounts/{ids}/info",
            headers=self.session_handler.json_headers,
            params={"include_interest_rate": "false"},
        )
        account_info_response.raise_for_status()
        return AccountsInfoResponse.parse_obj(account_info_response.json()).__root__
