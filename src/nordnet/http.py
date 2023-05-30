from typing import Any

from requests import Response

from nordnet.session import NordnetSession


class HttpHelper:
    def __init__(self, session: NordnetSession) -> None:
        self.session = session
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

    def get(self, url: str, headers: dict = {}, allow_redirects=False, **kwargs: Any) -> Response:
        headers = {**self.headers, **headers}
        return self.session.get(url, headers=headers, allow_redirects=allow_redirects, **kwargs)

    def post(self, url: str, headers: dict = {}, json_data: dict = {}, **kwargs: Any) -> Response:
        headers = {**self.headers, **headers}
        return self.session.post(url, headers=headers, json=json_data, **kwargs)


class HttpJsonHelper(HttpHelper):
    def __init__(self, session: NordnetSession) -> None:
        super().__init__(session)
        self.headers = {
            **self.headers,
            "Accept": "application/json",
            "Referer": "https://www.nordnet.dk/",
            "client-id": "NEXT",
        }
