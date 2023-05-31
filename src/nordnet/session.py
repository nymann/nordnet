import time
from typing import Any, Optional

import jwt
import requests
from requests.models import Response


class NordnetSession:  # noqa: WPS214 (only 2 public methods)
    def __init__(self, username: str, password: str):
        self._session: requests.Session = requests.Session()
        self._base_url = "https://www.nordnet.dk"
        self._password = password
        self._username = username
        self._session.cookies["cookie_consent"] = "necessary"
        self._session.cookies["nntheme"] = '{"a11y":false,"dark":"AUTO","osPref":"LIGHT"}'

    def get(self, url: str, protected: bool = True, **kwargs: Any) -> Response:
        if protected:
            self._check_token()
        response: requests.Response = self._session.get(self._base_url + url, **kwargs)
        return response

    def post(
        self,
        url: str,
        protected: bool = True,
        data: Optional[dict] = None,
        json: Optional[dict] = None,
        **kwargs: Any,
    ) -> Response:
        if protected:
            self._check_token()
        response: requests.Response = self._session.post(self._base_url + url, data=data, json=json, **kwargs)
        return response

    def _refresh_token(self) -> None:
        self._obtain_vital_cookies()
        self._login_user()

    def _headers(self) -> dict:
        return {
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

    def _obtain_vital_cookies(self) -> None:
        headers = {
            **self._headers(),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
        }
        self.get("/", headers=headers, allow_redirects=False, protected=False)
        self.get("/", headers=headers, protected=False)

    def _login_user(self) -> dict:
        headers = {
            **self._headers(),
            "Accept": "application/json",
            "Referer": "https://www.nordnet.dk/",
            "client-id": "NEXT",
            "Origin": self._base_url,
            "sub-client-id": "NEXT",
        }

        auth_response = self.post(
            url="/api/2/authentication/basic/login",
            headers=headers,
            json={"username": self._username, "password": self._password},
            protected=False,
        )
        auth_response.raise_for_status()
        return auth_response.json()

    def _check_token(self) -> None:
        token = self._session.cookies.get("NN-JWT")
        if token is None:
            self._refresh_token()
            return self._check_token()
        payload: dict[str, Any] = jwt.decode(
            token,
            algorithms=["HS256", "RS256"],
            options={"verify_signature": False},
            verify=False,
        )
        if payload["exp"] < time.time():
            self._refresh_token()
