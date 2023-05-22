import requests

from nordnet.models.accounts import Account
from nordnet.models.accounts import AccountsResponse
from nordnet.models.accounts_info import AccountInfo
from nordnet.models.accounts_info import AccountsInfoResponse


class NordnetApi:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.cookies["cookie_consent"] = "necessary"
        self.session.cookies["nntheme"] = '{"a11y":false,"dark":"AUTO","osPref":"LIGHT"}'
        self.headers = {
            "Accept-Language": "en-US,en;q=0.5",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "DNT": "1",
            "Pragma": "no-cache",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/113.0",
        }
        self._json_headers = {
            **self.headers,
            "Accept": "application/json",
            "Referer": "https://www.nordnet.dk/",
            "client-id": "NEXT",
            "content-type": "application/json",
        }
        self._base_url = "https://www.nordnet.dk"

    def login(self, username: str, password: str) -> dict:
        self._obtain_vital_cookies()
        self._login_anon()
        return self._login_user(username, password)

    def accounts(self) -> list[Account]:
        accounts_response = self.session.get(f"{self._base_url}/api/2/accounts", headers=self._json_headers)
        accounts_response.raise_for_status()
        return AccountsResponse.parse_obj(accounts_response.json()).__root__

    def accounts_info(self, accounts: list[Account]) -> list[AccountInfo]:
        ids = ",".join(str(acc.accid) for acc in accounts)
        account_info_response = self.session.get(
            f"{self._base_url}/api/2/accounts/{ids}/info",
            headers=self._json_headers,
            params={"include_interest_rate": "false"},
        )
        account_info_response.raise_for_status()
        return AccountsInfoResponse.parse_obj(account_info_response.json()).__root__

    def _obtain_vital_cookies(self) -> None:
        headers = {
            **self.headers,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
        }
        url = f"{self._base_url}/"
        self.session.get(url, headers=headers, allow_redirects=False)
        self.session.get(url, headers=headers)

    def _login_anon(self) -> None:
        login_response = self.session.get(
            f"{self._base_url}/api/2/login",
            headers=self._json_headers,
        )
        login_response.raise_for_status()

    def _login_user(self, username: str, password: str) -> dict:
        headers = {
            **self._json_headers,
            "Origin": self._base_url,
            "sub-client-id": "NEXT",
        }

        auth_response = self.session.post(
            f"{self._base_url}/api/2/authentication/basic/login",
            headers=headers,
            json={"username": username, "password": password},
        )
        auth_response.raise_for_status()
        return auth_response.json()
