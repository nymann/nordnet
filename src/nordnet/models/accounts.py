from pydantic import BaseModel


class Account(BaseModel):
    accno: int
    accid: int
    type: str
    atyid: int
    symbol: str
    account_code: str
    role: str
    default: bool
    alias: str


class AccountsResponse(BaseModel):
    __root__: list[Account]
