import discord
from discord.ext import commands
from discord import app_commands
import permissions as perms
from discord.ext import commands
import api_functions as api

def is_admin(interaction: discord.Interaction, permission: str = "admin") -> bool:
    return interaction.user.guild_permissions.administrator

def setup(bot: commands.Bot):
    @bot.tree.command(name="add_permission")
    @app_commands.describe(user="The user to grant the permission to", permission="The permission to grant")
    @app_commands.autocomplete(permission=perms.ac)
    @perms.require_permission("host")
    async def add_permission(interaction: discord.Interaction, user: discord.Member, permission: str):
        perms.add_permission(interaction.guild_id, user.id, permission)
        await interaction.response.send_message(f"Granted {permission} permission to {user.mention}.")

    @bot.tree.command(name="remove_permission")
    @app_commands.describe(user="The user to remove the permission from", permission="The permission to remove")
    @app_commands.autocomplete(permission=perms.ac)
    @perms.require_permission("host")
    async def remove_permission(interaction: discord.Interaction, user: discord.Member, permission: str):
        perms.remove_permission(interaction.guild_id, user.id, permission)
        await interaction.response.send_message(f"Removed {permission} permission from {user.mention}.")

    # -------------------------------------------------------------------------------------------------
    @bot.tree.command(name="start_game")
    @app_commands.describe(team_0="零小初始資金", team_1="一小初始資金", team_2="二小初始資金")
    @perms.require_permission("host")
    async def start_game(interaction: discord.Interaction, team_0: int, team_1: int, team_2: int):
        await interaction.response.defer()
        if perms.is_running(interaction.guild_id):
            await interaction.followup.send(embed=discord.Embed(title="遊戲已經開始了", description="請勿重複開始遊戲", color=0xff0000), ephemeral=True)
            return
    
        await interaction.followup.send(embeds=(*api.reset_all(), 
                                                api.set_balance("Zeroth", team_0), 
                                                api.set_balance("First", team_1), 
                                                api.set_balance("Second", team_2), 
                                                perms.set_running(interaction.guild_id, True)))
        
    @bot.tree.command(name="end_game")
    @perms.require_permission("host")
    async def end_game(interaction: discord.Interaction):
        await interaction.response.defer()
        if not perms.is_running(interaction.guild_id):
            await interaction.followup.send(embed=discord.Embed(title="遊戲已經結束了", description="請勿重複結束遊戲", color=0xff0000), ephemeral=True)
            return
        await interaction.followup.send(embed=perms.set_running(interaction.guild_id, False))

    @bot.tree.command(name="set_balance")
    @app_commands.describe(team_name="隊伍名稱", balance="初始資金")
    @perms.require_permission("host")
    async def set_balance(interaction: discord.Interaction, team_name: str, balance: int):
        await interaction.response.defer()
        await interaction.followup.send(embed=api.set_balance(team_name, balance))

    @bot.tree.command(name="set_holdings")
    @app_commands.describe(team_name="隊伍名稱", crypto_name="虛擬貨幣名稱", amount="持有數量")
    @app_commands.autocomplete(crypto_name=api.crypto_ac)
    @perms.require_permission("host")
    async def set_holdings(interaction: discord.Interaction, team_name: str, crypto_name: str, amount: int):
        await interaction.response.defer()
        await interaction.followup.send(embed=api.set_holdings(team_name, crypto_name, amount))
    
    @bot.tree.command(name="multiply_balance")
    @app_commands.describe(team_name="隊伍名稱", multiplier="乘數")
    @perms.require_permission("host")
    async def multiply_balance(interaction: discord.Interaction, team_name: str, multiplier: float):
        await interaction.response.defer()
        await interaction.followup.send(embed=api.multiply_balance(team_name, multiplier))

    @bot.tree.command(name="multiply_holdings")
    @app_commands.describe(team_name="隊伍名稱", crypto_name="虛擬貨幣名稱", multiplier="乘數")
    @app_commands.autocomplete(crypto_name=api.crypto_ac)
    @perms.require_permission("host")
    async def multiply_holdings(interaction: discord.Interaction, team_name: str, crypto_name: str, multiplier: float):
        await interaction.response.defer()
        await interaction.followup.send(embed=api.multiply_holdings(team_name, crypto_name, multiplier))

    @bot.tree.command(name="add_balance")
    @app_commands.describe(team_name="隊伍名稱", amount="增加的金額")
    @perms.require_permission("host")
    async def add_balance(interaction: discord.Interaction, team_name: str, amount: int):
        await interaction.response.defer()
        await interaction.followup.send(embed=api.add_balance(team_name, amount))
    
    @bot.tree.command(name="add_holdings")
    @app_commands.describe(team_name="隊伍名稱", crypto_name="虛擬貨幣名稱", amount="增加的持有數量")
    @app_commands.autocomplete(crypto_name=api.crypto_ac)
    @perms.require_permission("host")
    async def add_holdings(interaction: discord.Interaction, team_name: str, crypto_name: str, amount: int):
        await interaction.response.defer()
        await interaction.followup.send(embed=api.add_holdings(team_name, crypto_name, amount))

    @bot.tree.command(name="remove_balance")
    @app_commands.describe(team_name="隊伍名稱", amount="減少的金額")
    @perms.require_permission("host")
    async def remove_balance(interaction: discord.Interaction, team_name: str, amount: int):
        await interaction.response.defer()
        await interaction.followup.send(embed=api.remove_balance(team_name, amount))

    @bot.tree.command(name="remove_holdings")
    @app_commands.describe(team_name="隊伍名稱", crypto_name="虛擬貨幣名稱", amount="減少的持有數量")
    @app_commands.autocomplete(crypto_name=api.crypto_ac)
    @perms.require_permission("host")
    async def remove_holdings(interaction: discord.Interaction, team_name: str, crypto_name: str, amount: int):
        await interaction.response.defer()
        await interaction.followup.send(embed=api.remove_holdings(team_name, crypto_name, amount))