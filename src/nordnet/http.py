from typing import Any, Optional

from requests import Response

from nordnet.headers import Headers
from nordnet.session import NordnetSession


class HttpHelper:
    def __init__(self, session: NordnetSession) -> None:
        self._session = session
        self._headers = Headers().base()

    def get(self, url: str, extra_headers: Optional[dict] = None, allow_redirects=False, **kwargs: Any) -> Response:
        if extra_headers:
            headers = {**self._headers, **extra_headers}
        else:
            headers = self._headers
        return self._session.get(url, headers=headers, allow_redirects=allow_redirects, **kwargs)

    def post(self, url: str, extra_headers: Optional[dict] = None, json_data: dict = {}, **kwargs: Any) -> Response:
        if extra_headers:
            headers = {**self._headers, **extra_headers}
        else:
            headers = self._headers
        return self._session.post(url, headers=headers, json=json_data, **kwargs)


class HttpJsonHelper(HttpHelper):
    def __init__(self, session: NordnetSession) -> None:
        super().__init__(session)
        self._headers = Headers().json()
