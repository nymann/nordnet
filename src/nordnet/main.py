import typer

from nordnet.api import NordnetApi

app = typer.Typer()


@app.command()
def main(username: str, password: str) -> None:
    api = NordnetApi()
    api.login(username, password)
    acc_dict = dict()
    accounts = api.accounts()
    for acc in accounts:
        acc_dict[acc.accid] = acc.dict()
    accounts_info = api.accounts_info(accounts)
    for acc_info in accounts_info:
        acc_type = acc_dict[acc_info.accid]["type"]
        typer.echo(f"{acc_type}: {acc_info.equity.value} {acc_info.equity.currency}")


if __name__ == "__main__":
    app()
