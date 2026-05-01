import discord
from discord.ext import commands
from discord import app_commands
import logs as Logs
import permissions as perms
from discord.ext import commands

def is_admin(interaction: discord.Interaction, permission: str = "admin") -> bool:
    return interaction.user.guild_permissions.administrator

def setup(bot: commands.Bot):
    @bot.tree.command(name="add_permission")
    @app_commands.describe(user="The user to grant the permission to", permission="The permission to grant")
    @app_commands.autocomplete(permission=perms.ac)
    async def add_permission(interaction: discord.Interaction, user: discord.Member, permission):
        if not is_admin(interaction):
            await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
            return
        
        perms.add_permission(interaction.guild_id, user.id, permission)
        await interaction.response.send_message(f"Granted {permission} permission to {user.mention}.")

    @bot.tree.command(name="remove_permission")
    @app_commands.describe(user="The user to remove the permission from", permission="The permission to remove")
    @app_commands.autocomplete(permission=perms.ac)
    async def remove_permission(interaction: discord.Interaction, user: discord.Member, permission):
        if not is_admin(interaction):
            await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
            return
        
        perms.remove_permission(interaction.guild_id, user.id, permission)
        await interaction.response.send_message(f"Removed {permission} permission from {user.mention}.")

    # -------------------------------------------------------------------------------------------------
    @bot.tree.command(name="start_game")
    @app_commands.describe(team_0="零小初始資金", team_1="一小初始資金", team_2="二小初始資金")
    @perms.require_permission("host")
    async def start_game(interaction: discord.Interaction, team_0: int, team_1: int, team_2: int):
        if not is_admin(interaction):
            await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
            return
        perms.set_game_state(interaction.guild_id, True)
        
    @bot.tree.command(name="end_game")
    @perms.require_permission("host")
    async def end_game(interaction: discord.Interaction):
        if not is_admin(interaction):
            await interaction.response.send_message("You don't have permission to use this command", ephermeral=True)
            return
        perms.set_game_state(interaction.guild_id, False)

    