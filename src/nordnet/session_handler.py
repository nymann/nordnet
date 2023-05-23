from abc import ABC
from abc import abstractmethod

import requests


class SessionHandler(ABC):
    def __init__(self, session: requests.Session):
        self.session = session
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
        self.json_headers = {
            **self.headers,
            "Accept": "application/json",
            "Referer": "https://www.nordnet.dk/",
            "client-id": "NEXT",
            "content-type": "application/json",
        }
        self._base_url = "https://www.nordnet.dk"

    @abstractmethod
    def login(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def is_authenticated(self) -> bool:
        raise NotImplementedError


class UnauthenticatedSessionHandler(SessionHandler):
    def is_authenticated(self) -> bool:
        return False

    def login(self) -> dict:
        raise NotImplementedError("Call NordnetApi.login first")


class LoginSessionHandler(SessionHandler):
    def __init__(self, session: requests.Session, username: str, password: str):
        super().__init__(session)
        self.username = username
        self.password = password
        self.authenticated = False

    def login(self) -> dict:
        self.authenticated = True
        self._obtain_vital_cookies()
        self._login_anon()
        return self._login_user()

    def is_authenticated(self) -> bool:
        return self.authenticated

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
            headers=self.json_headers,
        )
        login_response.raise_for_status()

    def _login_user(self) -> dict:
        headers = {
            **self.json_headers,
            "Origin": self._base_url,
            "sub-client-id": "NEXT",
        }

        auth_response = self.session.post(
            f"{self._base_url}/api/2/authentication/basic/login",
            headers=headers,
            json={"username": self.username, "password": self.password},
        )
        auth_response.raise_for_status()
        return auth_response.json()
