from discord import app_commands
import discord


TEAM_NAMES = ["零小", "一小", "二小"]
TEAM_IDS = ["Zeroth", "First", "Second"]
TEAM_NAME_TO_ID = dict(zip(TEAM_NAMES, TEAM_IDS))
TEAM_ID_TO_NAME = dict(zip(TEAM_IDS, TEAM_NAMES))

CRYPTO_SYMBOLS = ["BTC", "ETH", "SOL"]
CRYPTO_NAMES = ["Bitcoin", "Ethereum", "Solana"]

API_LINK = "http://127.0.0.1:8000"

async def team_ac(interaction: discord.Interaction, current: str):
    return [
        app_commands.Choice(name=T, value=T)
        for T in TEAM_IDS
    ][:25]