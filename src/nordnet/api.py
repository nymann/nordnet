from nordnet.http import HttpJsonHelper
from nordnet.models.accounts import Account
from nordnet.models.accounts import AccountsResponse
from nordnet.models.accounts_info import AccountInfo
from nordnet.models.accounts_info import AccountsInfoResponse
from nordnet.session import NordnetSession


class NordnetApi:
    def __init__(self, username: str, password: str) -> None:
        self.requester = HttpJsonHelper(session=NordnetSession(username=username, password=password))

    def accounts(self) -> list[Account]:
        accounts_response = self.requester.get("/api/2/accounts")
        return AccountsResponse.parse_obj(accounts_response.json()).__root__

    def accounts_info(self, accounts: list[Account]) -> list[AccountInfo]:
        ids = ",".join(str(acc.accid) for acc in accounts)
        account_info_response = self.requester.get(
            f"/api/2/accounts/{ids}/info",
            params={"include_interest_rate": "false"},
        )
        return AccountsInfoResponse.parse_obj(account_info_response.json()).__root__
