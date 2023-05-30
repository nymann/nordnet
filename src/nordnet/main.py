import typer

from nordnet.api import NordnetApi
from nordnet.models.accounts import Account

app = typer.Typer()


@app.command()
def main(username: str, password: str) -> None:
    api = NordnetApi(username, password)
    acc_dict: dict[int, Account] = {}
    accounts = api.accounts()
    for acc in accounts:
        acc_dict[acc.accid] = acc
    accounts_info = api.accounts_info(accounts)
    for acc_info in accounts_info:
        acc = acc_dict[acc_info.accid]
        typer.echo(f"[{acc.type}]: {acc_info.equity.value} {acc_info.equity.currency}")


if __name__ == "__main__":
    app()
