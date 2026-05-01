import discord
from discord.ext import commands
from discord import app_commands
import logs as Logs
import permissions as perms
from discord.ext import commands

def is_admin_or_custom(interaction: discord.Interaction, permission: str = "admin") -> bool:
    is_discord_admin = interaction.user.guild_permissions.administrator
    has_custom_perm = perms.has_permission_a(interaction.guild_id, interaction.user.id, permission)
    return is_discord_admin or has_custom_perm

def setup(bot: commands.Bot):
    @bot.tree.command(name="add_permission", description="Add permission for a role.")
    @app_commands.describe(role="Role", perm="Permission")
    @app_commands.autocomplete(perm=perms.ac)
    async def set_permission(interaction: discord.Interaction, role: str, perm: str):
        if not is_admin_or_custom(interaction):
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return
        
        await interaction.response.defer()
        await Logs.log_command(interaction)
        perms.add_permission(interaction.guild_id, role, perm)

        await interaction.followup.send(f"Permission '{perm}' added for role '{role}'.")

    @bot.tree.command(name="remove_permission", description="Remove permission for a role.")
    @app_commands.describe(role="Role", perm="Permission")
    @app_commands.autocomplete(perm=perms.ac)
    async def remove_permission(interaction: discord.Interaction, role: str, perm: str):
        if not is_admin_or_custom(interaction):
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return
        
        await interaction.response.defer()
        await Logs.log_command(interaction)
        perms.remove_permission(interaction.guild_id, role, perm)

        await interaction.followup.send(f"Permission '{perm}' removed from role '{role}'.")

    @bot.tree.command(name="list_permissions", description="List permissions for a role.")
    @app_commands.describe(role="Role")
    async def list_permissions(interaction: discord.Interaction, role: str):
        if not is_admin_or_custom(interaction):
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return
        
        await interaction.response.defer()
        await Logs.log_command(interaction)
        perm_list = perms.get_permission(interaction.guild_id, role)
        perm = "".join([f"- {p}\n" for p in perm_list])
        if perm_list:
            await interaction.followup.send(f"Permissions for role '{role}':\n{perm}")

    @bot.tree.command(name="set_permission", description="Set permission for a role.")
    @app_commands.describe(role="Role", perm="Permission")
    @app_commands.autocomplete(perm=perms.ac)
    async def set_permission(interaction: discord.Interaction, role: str, perm: str):
        if not is_admin_or_custom(interaction):
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return
        
        await interaction.response.defer()
        await Logs.log_command(interaction)
        for p in perms.get_permission(interaction.guild_id, role):
            perms.remove_permission(interaction.guild_id, role, p)
            
        perms.add_permission(interaction.guild_id, role, perm)

        await interaction.followup.send(f"Permission '{perm}' set for role '{role}'.")

    @bot.command(name="debug")
    async def debug_addAP(ctx: commands.Context, *args):
        if args[0] == "--addAllPerms":
            role = args[1]
        for perm in perms.permissions:
            perms.add_permission(ctx.guild.id, role, perm)
        await ctx.send(f"Debug: Added permission '{perm}' for role '{role}'.", ephemeral=True)