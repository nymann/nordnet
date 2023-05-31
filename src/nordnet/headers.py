class Headers:
    def __init__(self) -> None:
        self._headers: dict[str, str] = {
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

    def base(self) -> dict[str, str]:
        return self._headers

    def json(self) -> dict[str, str]:
        return {
            **self._headers,
            "Accept": "application/json",
            "Referer": "https://www.nordnet.dk/",
            "client-id": "NEXT",
        }
