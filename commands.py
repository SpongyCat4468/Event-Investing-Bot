import discord
import api_functions as api
from discord import app_commands
def setup(bot: discord.ext.commands.Bot):
    @bot.tree.command(name="buy", description="購買虛擬貨幣")
    @app_commands.describe(crypto_name="虛擬貨幣名稱", amount="購買數量")
    async def buy(interaction: discord.Interaction, crypto_name: str, amount: int):
        user_id = interaction.user.id
        team_name = api.get_team_name(user_id)
        api.buy(user_id, crypto_name, amount)
        await interaction.channel.send(f"{team_name} 已買入 {amount} :otter:的 {crypto_name}")

    @bot.tree.command(name="sell", description="購買虛擬貨幣")
    @app_commands.describe(crypto_name="虛擬貨幣名稱", amount="購買數量")
    async def sell(interaction: discord.Interaction, crypto_name: str, amount: int):
        user_id = interaction.user.id
        team_name = api.get_team_name(user_id)
        api.sell(user_id, crypto_name, amount)
        await interaction.channel.send(f"{team_name} 已賣掉 {amount} :otter: 的 {crypto_name}")