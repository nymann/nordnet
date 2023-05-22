import requests

from nordnet.models.accounts import Account
from nordnet.models.accounts import AccountsResponse
from nordnet.models.accounts_info import AccountInfo
from nordnet.models.accounts_info import AccountsInfoResponse


class NordnetApi:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.cookies.set("cookie_consent", "necessary")
        self.session.cookies.set("nntheme", '{"a11y":false,"dark":"AUTO","osPref":"LIGHT"}')

    def login(self, username: str, password: str):
        self._obtain_vital_cookies()
        self._login_anon()
        return self._login_user(username, password)

    def accounts(self) -> list[Account]:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/113.0",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://www.nordnet.dk/",
            "client-id": "NEXT",
            "DNT": "1",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
        }
        accounts_response = self.session.get("https://www.nordnet.dk/api/2/accounts", headers=headers)
        accounts_response.raise_for_status()
        return AccountsResponse.parse_obj(accounts_response.json()).__root__

    def accounts_info(self, accounts: list[Account]) -> list[AccountInfo]:
        ids = ",".join(str(acc.accid) for acc in accounts)
        url = f"https://www.nordnet.dk/api/2/accounts/{ids}/info"

        querystring = {"include_interest_rate": "false"}

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/113.0",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.nordnet.dk/",
            "ntag": "d1485ddd-2bf1-4794-927a-7ba837285695",
            "client-id": "NEXT",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
        }
        account_info_response = self.session.get(url, headers=headers, params=querystring)
        account_info_response.raise_for_status()
        return AccountsInfoResponse.parse_obj(account_info_response.json()).__root__

    def _obtain_vital_cookies(self) -> None:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/113.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
        }
        url = "https://www.nordnet.dk/"
        self.session.get(url, headers=headers, allow_redirects=False)
        self.session.get(url, headers=headers)

    def _login_anon(self) -> None:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/113.0",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://www.nordnet.dk/",
            "client-id": "NEXT",
            "DNT": "1",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
        }
        login_response = self.session.get("https://www.nordnet.dk/api/2/login", headers=headers)
        login_response.raise_for_status()

    def _login_user(self, username: str, password: str):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/113.0",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://www.nordnet.dk/",
            "content-type": "application/json",
            "client-id": "NEXT",
            "sub-client-id": "NEXT",
            "Origin": "https://www.nordnet.dk",
            "DNT": "1",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
        }

        json_data = {
            "username": username,
            "password": password,
        }

        auth_response = self.session.post(
            "https://www.nordnet.dk/api/2/authentication/basic/login",
            headers=headers,
            json=json_data,
        )
        auth_response.raise_for_status()
        return auth_response.json()
