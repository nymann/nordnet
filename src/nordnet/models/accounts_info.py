from pydantic import BaseModel


class AccountCredit(BaseModel):
    currency: str
    value: float


class Collateral(AccountCredit):
    pass


class PawnValue(AccountCredit):
    pass


class TradingPower(AccountCredit):
    pass


class ShortPositionsMargin(AccountCredit):
    pass


class BuyOrdersValue(AccountCredit):
    pass


class LoanLimit(AccountCredit):
    pass


class ForwardSum(AccountCredit):
    pass


class FutureSum(AccountCredit):
    pass


class Interest(AccountCredit):
    pass


class AccountSum(AccountCredit):
    pass


class UnrealizedFutureProfitLoss(AccountCredit):
    pass


class OwnCapital(BaseModel):
    value: float
    currency: str


class OwnCapitalMorning(AccountCredit):
    pass


class FullMarketvalue(AccountCredit):
    pass


class Equity(OwnCapital):
    pass


class AccountInfo(BaseModel):
    account_credit: AccountCredit
    collateral: Collateral
    pawn_value: PawnValue
    trading_power: TradingPower
    short_positions_margin: ShortPositionsMargin
    buy_orders_value: BuyOrdersValue
    loan_limit: LoanLimit
    forward_sum: ForwardSum
    future_sum: FutureSum
    account_currency: str
    interest: Interest
    account_sum: AccountSum
    unrealized_future_profit_loss: UnrealizedFutureProfitLoss
    own_capital: OwnCapital
    own_capital_morning: OwnCapitalMorning
    full_marketvalue: FullMarketvalue
    account_code: str
    registration_date: str
    accno: int
    accid: int
    equity: Equity


class AccountsInfoResponse(BaseModel):
    __root__: list[AccountInfo]
