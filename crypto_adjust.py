import random
import requests
import api_functions as api
from discord.ext import tasks

from data import API_LINK
from data import CRYPTO_CHANGE_RATE

CRYPTOS = ["BTC", "ETH", "LTC"]

def update_prices():
    for symbol in CRYPTOS:
        current = api.get_crypto_price(symbol)  # fetch current price first
        new_price = current * random.uniform(1 - CRYPTO_CHANGE_RATE, 1 + CRYPTO_CHANGE_RATE)  # ±5% change
        requests.patch(
            f"{API_LINK}/cryptos/{symbol}/price",
            json={"price": round(new_price, 2)}
        )

@tasks.loop(minutes=1)
async def update_prices_loop():
    update_prices()