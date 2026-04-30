import requests
import json

API_LINK = "http://127.0.0.1:8000"


# ── Mapping ───────────────────────────────────────────────────────────────────

def get_team_name(user_id) -> str:
    """Map a Discord user_id to a team name by looking up id.json."""
    with open("id.json", "r") as f:
        id_map: dict = json.load(f)
    team = id_map.get(str(user_id))
    if team is None:
        raise ValueError(f"User ID {user_id} is not registered in id.json")
    return team


# ── Trading ───────────────────────────────────────────────────────────────────

def buy(user_id, crypto_name: str, amount: float) -> dict:
    """Buy `amount` units of `crypto_name` for the team linked to `user_id`."""
    response = requests.post(
        f"{API_LINK}/trade/buy",
        json={
            "team_name": get_team_name(user_id),
            "crypto_symbol": crypto_name.upper(),
            "quantity": abs(amount),
        },
    )
    response.raise_for_status()
    return response.json()


def sell(user_id, crypto_name: str, amount: float) -> dict:
    """Sell `amount` units of `crypto_name` for the team linked to `user_id`."""
    response = requests.post(
        f"{API_LINK}/trade/sell",
        json={
            "team_name": get_team_name(user_id),
            "crypto_symbol": crypto_name.upper(),
            "quantity": abs(amount),
        },
    )
    response.raise_for_status()
    return response.json()


# ── Queries ───────────────────────────────────────────────────────────────────

def get_balance(user_id) -> float:
    """Return the team's current USD cash balance."""
    team_name = get_team_name(user_id)
    response = requests.get(f"{API_LINK}/teams/{team_name}")
    response.raise_for_status()
    return response.json()["balance"]


def get_crypto_price(crypto_name: str) -> float:
    """Return the current price of a cryptocurrency."""
    response = requests.get(f"{API_LINK}/cryptos/{crypto_name.upper()}")
    response.raise_for_status()
    return response.json()["current_price"]


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