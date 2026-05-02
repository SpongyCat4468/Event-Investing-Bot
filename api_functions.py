import requests
import json
import discord
from discord import app_commands
from data import API_LINK
import data



# ── Mapping ───────────────────────────────────────────────────────────────────

def get_leaderboard() -> dict[str, float]:
    """Return teams ranked by total portfolio value as an ordered dict."""
    response = requests.get(f"{API_LINK}/leaderboard")
    response.raise_for_status()
    return {team["name"]: team["total_portfolio_value"] for team in response.json()}

def get_team_name(id: int | str) -> str:
    if id.__class__ == int:
        """Map a Discord user_id to a team name by looking up id.json."""
        with open("id.json", "r") as f:
            id_map: dict = json.load(f)
        team = id_map.get(str(id))
        if team is None:
            raise ValueError(f"User ID {id} is not registered in id.json")
        return data.TEAM_ID_TO_NAME[team]
    elif id.__class__ == str:
        return data.TEAM_ID_TO_NAME[id]

def get_team_id(user_id) -> str:
    with open("id.json", "r") as f:
        id_map: dict = json.load(f)
    team = id_map.get(str(user_id))
    if team is None:
        raise ValueError(f"User ID {user_id} is not registered in id.json")
    return team


# ── Set ───────────────────────────────────────────────────────────────────

def buy(user_id, crypto_name: str, amount: float) -> discord.Embed:
    """Buy `amount` units of `crypto_name` for the team linked to `user_id`."""
    if amount <= 0:
        return discord.Embed(title=f"交易失敗: 購買數量必須大於 0", color=0xff0000)
    response = requests.post(
        f"{API_LINK}/trade/buy",
        json={
            "team_name": get_team_id(user_id),
            "crypto_symbol": crypto_name.upper(),
            "quantity": abs(amount),
        },
    )
    if response.status_code == 400:
        return discord.Embed(title=f"交易失敗: 餘額不足", color=0xff0000)
    elif response.status_code == 200:
        return discord.Embed(title=f"{get_team_name(user_id)} 已買入 {amount} :otter:的 {crypto_name}", color=0x00ff00)
    elif response.status_code == 404:
        if response.json().get("detail").find("Crypto") != -1:
            return discord.Embed(title=f"交易失敗: 找不到 {crypto_name.upper()} 這種虛擬貨幣", color=0xff0000)
        elif response.json().get("detail").find("Team") != -1:
            return discord.Embed(title=f"交易失敗: 找不到 {get_team_name(user_id)} 這個隊伍", color=0xff0000)
    else:
        response.raise_for_status()


def sell(user_id, crypto_name: str, amount: float) -> discord.Embed:
    if amount <= 0:
        return discord.Embed(title=f"交易失敗: 賣出數量必須大於 0", color=0xff0000)
    """Sell `amount` units of `crypto_name` for the team linked to `user_id`."""
    response = requests.post(
        f"{API_LINK}/trade/sell",
        json={
            "team_name": get_team_id(user_id),
            "crypto_symbol": crypto_name.upper(),
            "quantity": abs(amount),
        },
    )
    if response.status_code == 400:
        return discord.Embed(title=f"交易失敗: 持有的虛擬貨幣不足", color=0xff0000)
    elif response.status_code == 404:
        if response.json().get("detail").find("Crypto") != -1:
            return discord.Embed(title=f"交易失敗: 找不到 {crypto_name.upper()} 這種虛擬貨幣", color=0xff0000)
        elif response.json().get("detail").find("Team") != -1:
            return discord.Embed(title=f"交易失敗: 找不到 {get_team_name(user_id)} 這個隊伍", color=0xff0000)
    elif response.status_code == 200:
        return discord.Embed(title=f"{get_team_name(user_id)} 已賣出 {amount} :otter:的 {crypto_name}", color=0xff0000)
    else:
        response.raise_for_status()

def reset_all() -> tuple[discord.Embed, discord.Embed, discord.Embed]:
    embeds = []
    for idx, team in enumerate(data.TEAM_IDS):
        response_balance = requests.post(
            f"{API_LINK}/teams/{team}/reset/balance",
            params={"balance": 0}
        )
        response_holdings = requests.post(
            f"{API_LINK}/teams/{team}/reset/holdings",
            json={"BTC": 0, "ETH": 0, "SOL": 0}
        )
        balance_success = response_balance.status_code == 200
        holdings_success = response_holdings.status_code == 200

        embeds.append(discord.Embed(
            title=f"{data.TEAM_NAMES[idx]} 已重置", 
            description=f"餘額重置{'成功' if balance_success else '失敗 ' + response_balance.json()['detail']}, \n持有量重置{'成功' if holdings_success else '失敗 ' + response_holdings.json()['detail']}",
            color=0x00ff00 if balance_success and holdings_success else 0xff0000
        ))
    return embeds

def set_balance(team_name: str, balance: int) -> discord.Embed:
    response = requests.post(
        f"{API_LINK}/teams/{team_name}/reset/balance",
        params={"balance": balance}
    )
    if response.status_code == 200:
        return discord.Embed(title=f"{get_team_name(team_name)} 的餘額已設置為 ${balance}", color=0x00ff00)
    else:
        return discord.Embed(title=f"{get_team_name(team_name)} 的餘額設置失敗", color=0xff0000)
    
def set_holdings(team_name: str, crypto_symbol: str, quantity: int) -> discord.Embed:
    response = requests.post(
        f"{API_LINK}/teams/{team_name}/reset/holdings",
        json={crypto_symbol: quantity}
    )
    if response.status_code == 200:
        return discord.Embed(title=f"{get_team_name(team_name)} 的 {crypto_symbol} 持有量已設置為 {quantity}", color=0x00ff00)
    else:
        return discord.Embed(title=f"{get_team_name(team_name)} 的 {crypto_symbol} 持有量設置失敗", color=0xff0000)
    
def multiply_balance(team_id: str, multiplier: float) -> discord.Embed:
    portfolio = get_portfolio_team(team_id)
    new_balance = portfolio["balance"] * multiplier
    response = requests.post(
        f"{API_LINK}/teams/{team_id}/reset/balance",
        params={"balance": new_balance}
    )
    if response.status_code == 200:
        return discord.Embed(title=f"{get_team_name(team_id)} 的餘額已乘以 {multiplier}，新餘額為 ${new_balance:.2f}", color=0x00ff00)
    else:
        return discord.Embed(title=f"{get_team_name(team_id)} 的餘額乘法操作失敗", color=0xff0000)
    
def multiply_holdings(team_id: str, crypto_symbol: str, multiplier: float) -> discord.Embed:
    portfolio = get_portfolio_team(team_id)
    current_quantity = 0
    for holding in portfolio["holdings"]:
        if holding["crypto_symbol"] == crypto_symbol:
            current_quantity = holding["quantity"]
            break
    new_quantity = current_quantity * multiplier
    response = requests.post(
        f"{API_LINK}/teams/{team_id}/reset/holdings",
        json={crypto_symbol: new_quantity}
    )
    if response.status_code == 200:
        return discord.Embed(title=f"{get_team_name(team_id)} 的 {crypto_symbol} 持有量已乘以 {multiplier}，新持有量為 {new_quantity:.4f}", color=0x00ff00)
    else:
        return discord.Embed(title=f"{get_team_name(team_id)} 的 {crypto_symbol} 持有量乘法操作失敗", color=0xff0000)
    
def add_balance(team_id, amount: float) -> discord.Embed:
    portfolio = get_portfolio_team(team_id)
    new_balance = portfolio["balance"] + amount
    response = requests.post(
        f"{API_LINK}/teams/{team_id}/reset/balance",
        params={"balance": new_balance}
    )
    if response.status_code == 200:
        return discord.Embed(title=f"{get_team_name(team_id)} 的餘額已增加 {amount}，新餘額為 ${new_balance:.2f}", color=0x00ff00)
    else:
        return discord.Embed(title=f"{get_team_name(team_id)} 的餘額增加操作失敗", color=0xff0000)
    
def remove_balance(team_id, amount: float) -> discord.Embed:
    portfolio = get_portfolio_team(team_id)
    new_balance = portfolio["balance"] - amount
    response = requests.post(
        f"{API_LINK}/teams/{team_id}/reset/balance",
        params={"balance": new_balance}
    )
    if response.status_code == 200:
        return discord.Embed(title=f"{get_team_name(team_id)} 的餘額已減少 {amount}，新餘額為 ${new_balance:.2f}", color=0x00ff00)
    else:
        return discord.Embed(title=f"{get_team_name(team_id)} 的餘額減少操作失敗", color=0xff0000)
    
def add_holdings(team_id, crypto_symbol: str, amount: float) -> discord.Embed:
    portfolio = get_portfolio_team(team_id)
    current_quantity = 0
    for holding in portfolio["holdings"]:
        if holding["crypto_symbol"] == crypto_symbol:
            current_quantity = holding["quantity"]
            break
    new_quantity = current_quantity + amount
    response = requests.post(
        f"{API_LINK}/teams/{team_id}/reset/holdings",
        json={crypto_symbol: new_quantity}
    )
    if response.status_code == 200:
        return discord.Embed(title=f"{get_team_name(team_id)} 的 {crypto_symbol} 持有量已增加 {amount}，新持有量為 {new_quantity:.4f}", color=0x00ff00)
    else:
        return discord.Embed(title=f"{get_team_name(team_id)} 的 {crypto_symbol} 持有量增加操作失敗", color=0xff0000)
    
def remove_holdings(team_id, crypto_symbol: str, amount: float) -> discord.Embed:
    portfolio = get_portfolio_team(team_id)
    current_quantity = 0
    for holding in portfolio["holdings"]:
        if holding["crypto_symbol"] == crypto_symbol:
            current_quantity = holding["quantity"]
            break
    new_quantity = current_quantity - amount
    response = requests.post(
        f"{API_LINK}/teams/{team_id}/reset/holdings",
        json={crypto_symbol: new_quantity}
    )
    if response.status_code == 200:
        return discord.Embed(title=f"{get_team_name(team_id)} 的 {crypto_symbol} 持有量已減少 {amount}，新持有量為 {new_quantity:.4f}", color=0x00ff00)
    else:
        return discord.Embed(title=f"{get_team_name(team_id)} 的 {crypto_symbol} 持有量減少操作失敗", color=0xff0000)

# ── Get ───────────────────────────────────────────────────────────────────

async def crypto_autocomplete(interaction: discord.Interaction, current: str):
    return [
        app_commands.Choice(name=item, value=item)
        for item in data.CRYPTO_SYMBOLS
    ]

crypto_ac = crypto_autocomplete

def get_balance(user_id) -> float:
    """Return the team's current USD cash balance."""
    team_name = get_team_id(user_id)
    response = requests.get(f"{API_LINK}/teams/{team_name}")
    response.raise_for_status()
    return response.json()["balance"]

def get_crypto_price(crypto_name: str) -> float:
    """Return the current price of a cryptocurrency."""
    response = requests.get(f"{API_LINK}/cryptos/{crypto_name.upper()}")
    response.raise_for_status()
    return response.json()["current_price"]

def get_all_prices() -> dict[str, float]:
    """Return all cryptocurrencies and their current prices as a dict."""
    response = requests.get(f"{API_LINK}/cryptos")
    response.raise_for_status()
    return {(crypto["symbol"], crypto["name"]): crypto["current_price"] for crypto in response.json()}

def get_portfolio(user_id) -> dict:
    """Return the team's full portfolio: balance, holdings, and total value."""
    team_name = get_team_id(user_id)
    response = requests.get(f"{API_LINK}/teams/{team_name}")
    response.raise_for_status()
    return response.json()

def get_portfolio_team(team_id) -> dict:
    """Return the team's full portfolio: balance, holdings, and total value."""
    response = requests.get(f"{API_LINK}/teams/{team_id}")
    response.raise_for_status()
    return response.json()


def get_trade_history(user_id, limit: int = 5) -> list[dict]:
    """Return the team's trade history, newest first, capped at `limit` entries."""
    team_name = get_team_id(user_id)
    response = requests.get(f"{API_LINK}/teams/{team_name}/trades")
    response.raise_for_status()
    return response.json()[:limit]

def update_prices(crypto_name: str) -> None:
    """Trigger the API to update cryptocurrency prices from CoinGecko."""
    response = requests.post(f"{API_LINK}/cryptos/{crypto_name.upper()}", json={"action": "update"})
    response.raise_for_status()

# ── Display ───────────────────────────────────────────────────────────────────

def show_database():
    # ── Cryptocurrencies ──────────────────────────────────────────────────────
    cryptos: list[dict] = requests.get(f"{API_LINK}/cryptos").json()

    print("=" * 65)
    print("CRYPTOCURRENCIES")
    print("=" * 65)
    print(f"  {'Symbol':<8} {'Name':<15} {'Price (USD)':>14}")
    print("  " + "-" * 42)
    for c in cryptos:
        print(
            f"  {c['symbol']:<8} {c['name']:<15}"
            f" {c['current_price']:>14,.4f}"
        )

    # ── Teams ─────────────────────────────────────────────────────────────────
    teams: list[dict] = requests.get(f"{API_LINK}/teams").json()

    for team in teams:
        team_name = team["name"]
        print()
        print("=" * 65)
        print(f"  TEAM: {team_name}")
        print("=" * 65)

        # Full detail: balance + holdings + portfolio value
        detail: dict = requests.get(f"{API_LINK}/teams/{team_name}").json()
        holdings: list[dict] = detail["holdings"]

        print(f"  Cash balance     : ${detail['balance']:>12,.2f}")
        print(f"  Portfolio value  : ${detail['total_portfolio_value']:>12,.2f}")

        print()
        if holdings:
            print(f"  {'Symbol':<8} {'Qty':>12} {'Cur Price':>12} {'Value':>12}")
            print("  " + "-" * 50)
            for h in holdings:
                print(
                    f"  {h['crypto_symbol']:<8}"
                    f" {h['quantity']:>12.4f}"
                    f" {h['current_price']:>12.4f}"
                    f" {h['current_value']:>12.2f}"
                )
        else:
            print("  (no holdings)")

        # Recent transactions
        txns: list[dict] = requests.get(f"{API_LINK}/teams/{team_name}/trades").json()
        print()
        if txns:
            print(f"  Recent trades (last 5 of {len(txns)}):")
            print(f"  {'Type':<5} {'Symbol':<8} {'Qty':>10} {'Price':>12} {'Total':>12}  Timestamp")
            print("  " + "-" * 65)
            for t in txns[:5]:  # API returns newest-first
                print(
                    f"  {t['trade_type'].upper():<5} {t['crypto_symbol']:<8}"
                    f" {t['quantity']:>10.4f} {t['price_at_trade']:>12.4f}"
                    f" {t['total_value']:>12.2f}  {t['executed_at'][:19]}"
                )
        else:
            print("  (no trades)")

    # ── Leaderboard ───────────────────────────────────────────────────────────
    print()
    print("=" * 65)
    print("LEADERBOARD")
    print("=" * 65)
    board: list[dict] = requests.get(f"{API_LINK}/leaderboard").json()
    for i, team in enumerate(board, 1):
        print(f"  #{i}  {team['name']:<10}  ${team['total_portfolio_value']:>12,.2f}")

    print()
    print("=" * 65)


if __name__ == "__main__":
    show_database()