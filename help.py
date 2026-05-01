import discord
def setup(bot):
    @bot.tree.command(name="help", description="查看所有指令說明")
    async def help(interaction: discord.Interaction):
        await interaction.response.defer()

        embed = discord.Embed(title="指令說明", color=0x5865F2)

        embed.add_field(
            name="交易",
            value=(
                "`/buy <crypto_name> <amount>` — 買入指定數量的虛擬貨幣\n"
                "`/sell <crypto_name> <amount>` — 賣出指定數量的虛擬貨幣"
            ),
            inline=False,
        )

        embed.add_field(
            name="持倉",
            value=(
                "`/balance` — 查詢團隊現金餘額\n"
                "`/portfolio` — 查看持倉、市值與總資產\n"
                "`/history` — 查看最近 5 筆交易紀錄\n"
                "`/whoami` — 查看你的團隊名稱"
            ),
            inline=False,
        )

        embed.add_field(
            name="市場",
            value=(
                "`/price <crypto_name>` — 查詢單一幣種價格\n"
                "`/prices` — 查詢所有幣種市場價格\n"
                "`/leaderboard` — 查看所有隊伍排行榜"
            ),
            inline=False,
        )

        embed.set_footer(text="輸入 <crypto_name> 時請使用幣種代號，例如：BTC、ETH")
        await interaction.followup.send(embed=embed)

    @bot.tree.command(name="host_help", description="查看主持人指令說明")
    async def host_help(interaction: discord.Interaction):
        await interaction.response.defer()
        embed = discord.Embed(title="主持人指令說明", color=0xFF5733)

        embed.add_field(
            name="遊戲控制",
            value=(
                "`/start_game <team_0> <team_1> <team_2>` — 開始遊戲並設定三隊初始資金\n"
                "`/end_game` — 結束遊戲"
            ),
            inline=False,
        )

        embed.add_field(
            name="隊伍管理",
            value=(
                "`/set_balance <team_name> <balance>` — 設定指定隊伍的現金餘額\n"
                "`/set_holdings <team_name> <crypto_name> <amount>` — 設定指定隊伍的持幣數量"
            ),
            inline=False,
        )

        embed.add_field(
            name="權限管理",
            value=(
                "`/add_permission <user> <permission>` — 授予使用者指定權限\n"
                "`/remove_permission <user> <permission>` — 移除使用者指定權限"
            ),
            inline=False,
        )

        embed.set_footer(text="此指令僅限主持人使用")
        await interaction.followup.send(embed=embed, ephemeral=True)