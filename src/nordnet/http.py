from typing import Any, Optional

from requests import Response

from nordnet.headers import Headers
from nordnet.session import NordnetSession


class HttpHelper:
    def __init__(self, session: NordnetSession) -> None:
        self._session = session
        self._headers = Headers().base()

    def get(
        self,
        url: str,
        extra_headers: Optional[dict] = None,
        allow_redirects: bool = False,
        **kwargs: Any,
    ) -> Response:
        return self._session.get(
            url,
            headers=self._create_headers(extra_headers),
            allow_redirects=allow_redirects,
            **kwargs,
        )

    def post(
        self,
        url: str,
        extra_headers: Optional[dict] = None,
        json_data: Optional[dict] = None,
        **kwargs: Any,
    ) -> Response:
        return self._session.post(
            url,
            headers=self._create_headers(extra_headers),
            json=json_data,
            **kwargs,
        )

    def _create_headers(self, extra_headers: Optional[dict] = None) -> dict:
        if extra_headers:
            return {**self._headers, **extra_headers}
        return self._headers


class HttpJsonHelper(HttpHelper):
    def __init__(self, session: NordnetSession) -> None:
        super().__init__(session)
        self._headers = Headers().json()
