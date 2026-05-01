import discord
import api_functions as api
from discord import app_commands
import permissions as perms


def setup(bot: discord.ext.commands.Bot):
    @bot.tree.command(name="buy", description="購買虛擬貨幣")
    @app_commands.describe(crypto_name="虛擬貨幣名稱", amount="購買數量")
    @app_commands.autocomplete(crypto_name=api.crypto_ac)
    async def buy(interaction: discord.Interaction, crypto_name: str, amount: int):
        await interaction.response.defer()
        if not perms.is_running(interaction.guild_id):
            await interaction.followup.send(embed=discord.Embed(title="遊戲尚未開始", description="請稍後再試", color=0xff0000), ephemeral=True)
            return
        user_id = interaction.user.id
        await interaction.followup.send(embed=api.buy(user_id, crypto_name, amount))

    @bot.tree.command(name="sell", description="購買虛擬貨幣")
    @app_commands.describe(crypto_name="虛擬貨幣名稱", amount="購買數量")
    @app_commands.autocomplete(crypto_name=api.crypto_ac)
    async def sell(interaction: discord.Interaction, crypto_name: str, amount: int):
        await interaction.response.defer()
        if not perms.is_running(interaction.guild_id):
            await interaction.followup.send(embed=discord.Embed(title="遊戲尚未開始", description="請稍後再試", color=0xff0000), ephemeral=True)
            return
        user_id = interaction.user.id
        team_name = api.get_team_name(user_id)
        await interaction.followup.send(embed=api.sell(user_id, crypto_name, amount))

    @bot.tree.command(name="balance", description="查詢團隊餘額")
    async def balance(interaction: discord.Interaction):
        await interaction.response.defer()
        if not perms.is_running(interaction.guild_id):
            await interaction.followup.send(embed=discord.Embed(title="遊戲尚未開始", description="請稍後再試", color=0xff0000), ephemeral=True)
            return
        user_id = interaction.user.id
        team_name = api.get_team_name(user_id)
        balance = api.get_balance(user_id)
        await interaction.followup.send(embed=discord.Embed(title=f"{team_name} 的餘額", description=f"你的小隊目前有 ${balance}", color=0x00ff00))

    @bot.tree.command(name="whoami", description="查詢團隊名稱")
    async def whoami(interaction: discord.Interaction):
        await interaction.response.defer()
        if not perms.is_running(interaction.guild_id):
            await interaction.followup.send(embed=discord.Embed(title="遊戲尚未開始", description="請稍後再試", color=0xff0000), ephemeral=True)
            return
        user_id = interaction.user.id
        team_name = api.get_team_name(user_id)
        await interaction.followup.send(embed=discord.Embed(title=f"你是 {team_name} 的成員!", color=0x00ff00))

    @bot.tree.command(name="leaderboard", description="查詢排行榜")
    async def leaderboard(interaction: discord.Interaction):
        await interaction.response.defer()
        if not perms.is_running(interaction.guild_id):
            await interaction.followup.send(embed=discord.Embed(title="遊戲尚未開始", description="請稍後再試", color=0xff0000), ephemeral=True)
            return
        board = api.get_leaderboard()
        embed = discord.Embed(title="排行榜", color=0x00ff00)
        for i, (team, value) in enumerate(board.items(), 1):
            embed.add_field(
                name=f"#{i} {api.get_team_name(team)}",
                value=f"${value:,.2f}",
                inline=False
            )
        await interaction.followup.send(embed=embed)

    @bot.tree.command(name="price", description="查詢單一虛擬貨幣價格")
    @app_commands.describe(crypto_name="虛擬貨幣名稱 (例: BTC)")
    @app_commands.autocomplete(crypto_name=api.crypto_ac)
    async def price(interaction: discord.Interaction, crypto_name: str):
        await interaction.response.defer()
        if not perms.is_running(interaction.guild_id):
            await interaction.followup.send(embed=discord.Embed(title="遊戲尚未開始", description="請稍後再試", color=0xff0000), ephemeral=True)
            return
        current_price = api.get_crypto_price(crypto_name)
        embed = discord.Embed(
            title=f"{crypto_name.upper()} 目前價格",
            description=f"**${current_price:,.4f}**",
            color=0xf0b90b,
        )
        await interaction.followup.send(embed=embed)
 
    @bot.tree.command(name="prices", description="查詢所有虛擬貨幣價格")
    async def prices(interaction: discord.Interaction):
        await interaction.response.defer()
        if not perms.is_running(interaction.guild_id):
            await interaction.followup.send(embed=discord.Embed(title="遊戲尚未開始", description="請稍後再試", color=0xff0000), ephemeral=True)
            return
        all_cryptos = api.get_all_prices()
        embed = discord.Embed(title="市場價格", color=0xf0b90b)
        for (symbol, name), price in all_cryptos.items():
            embed.add_field(
                name=f"{name} ({symbol})",
                value=f"${price:,.4f}",
                inline=False,
            )
        await interaction.followup.send(embed=embed)
 
    @bot.tree.command(name="portfolio", description="查詢團隊持倉")
    async def portfolio(interaction: discord.Interaction):
        await interaction.response.defer()
        if not perms.is_running(interaction.guild_id):
            await interaction.followup.send(embed=discord.Embed(title="遊戲尚未開始", description="請稍後再試", color=0xff0000), ephemeral=True)
            return
        user_id = interaction.user.id
        team_name = api.get_team_name(user_id)
        data = api.get_portfolio(user_id)
        holdings = data["holdings"]
 
        embed = discord.Embed(title=f"{team_name} 的持倉", color=0x00bfff)
        embed.add_field(name="現金餘額", value=f"${data['balance']:,.2f}", inline=True)
        embed.add_field(name="總資產", value=f"${data['total_portfolio_value']:,.2f}", inline=True)
 
        if holdings:
            embed.add_field(name="\u200b", value="**持有幣種**", inline=False)
            for h in holdings:
                embed.add_field(
                    name=f"{h['crypto_symbol']}  x{h['quantity']:.4f}",
                    value=f"現價 ${h['current_price']:,.4f}\n市值 ${h['current_value']:,.2f}",
                    inline=True,
                )
        else:
            embed.add_field(name="\u200b", value="目前沒有持倉", inline=False)
 
        await interaction.followup.send(embed=embed)
 
    @bot.tree.command(name="history", description="查詢團隊近期交易紀錄")
    async def history(interaction: discord.Interaction):
        await interaction.response.defer()
        if not perms.is_running(interaction.guild_id):
            await interaction.followup.send(embed=discord.Embed(title="遊戲尚未開始", description="請稍後再試", color=0xff0000), ephemeral=True)
            return
        user_id = interaction.user.id
        team_name = api.get_team_name(user_id)
        trades = api.get_trade_history(user_id, limit=5)
 
        embed = discord.Embed(title=f"{team_name} 的交易紀錄", color=0x9b59b6)
 
        if not trades:
            embed.description = "尚無交易紀錄"
        else:
            for t in trades:
                is_buy = t["trade_type"] == "buy"
                emoji = "🟢" if is_buy else "🔴"
                action = "買入" if is_buy else "賣出"
                embed.add_field(
                    name=f"{emoji} {action} {t['crypto_symbol']}",
                    value=(
                        f"數量：{t['quantity']:.4f}\n"
                        f"單價：${t['price_at_trade']:,.4f}\n"
                        f"總額：${t['total_value']:,.2f}\n"
                        f"時間：{t['executed_at'][:19]}"
                    ),
                    inline=True,
                )
 
        await interaction.followup.send(embed=embed)