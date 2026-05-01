import discord
import sqlite3
from discord import app_commands
from discord.ext import commands
from functools import wraps

DB_PATH = "data.db"
db = sqlite3.connect(DB_PATH)
cursor = db.cursor()

permissions = [
    "host"
]

def is_running(guild_id: int) -> bool:
    """Check if the game is currently running in a guild."""
    cursor.execute(
        "SELECT is_running FROM game_state WHERE guild_id = ?",
        (guild_id,)
    )
    row = cursor.fetchone()
    return bool(row[0]) if row else False

def set_running(guild_id: int, state: bool) -> None:
    """Set the game running state for a guild."""
    cursor.execute(
        "INSERT INTO game_state (guild_id, is_running) VALUES (?, ?)"
        " ON CONFLICT(guild_id) DO UPDATE SET is_running = excluded.is_running",
        (guild_id, int(state))
    )
    db.commit()

async def ac(interaction: discord.Interaction, current: str):
    return [
        app_commands.Choice(name=p, value=p)
        for p in permissions
        if current.lower() in p.lower()
    ][:25]


def get_permission(guild_id: int, user_id: int) -> tuple[str]:
    """Return all permissions a user has in a guild."""
    cursor.execute(
        "SELECT permission FROM user_permissions WHERE guild_id = ? AND user_id = ?",
        (guild_id, user_id)
    )
    return tuple(row[0] for row in cursor.fetchall())


def add_permission(guild_id: int, user_id: int, permission: str) -> None:
    """Assign a permission to a user in a guild."""
    cursor.execute(
        "INSERT OR IGNORE INTO user_permissions (guild_id, user_id, permission) VALUES (?, ?, ?)",
        (guild_id, user_id, permission)
    )
    db.commit()


def remove_permission(guild_id: int, user_id: int, permission: str) -> None:
    """Remove a permission from a user in a guild."""
    cursor.execute(
        "DELETE FROM user_permissions WHERE guild_id = ? AND user_id = ? AND permission = ?",
        (guild_id, user_id, permission)
    )
    db.commit()


def has_permission(interaction: discord.Interaction, permission: str) -> bool:
    """Check if the interaction author has a given permission in the guild."""
    cursor.execute(
        "SELECT 1 FROM user_permissions WHERE guild_id = ? AND user_id = ? AND permission = ? LIMIT 1",
        (interaction.guild.id, interaction.user.id, permission)
    )
    return cursor.fetchone() is not None

def require_permission(permission: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(Interaction, *args, **kwargs):
            if isinstance(Interaction, discord.Interaction):
                if not has_permission(Interaction, permission):
                    if not Interaction.response.is_done():
                        await Interaction.response.send_message(
                            "You don't have the permission to execute this command.",
                            ephemeral=True
                        )
                    else:
                        await Interaction.followup.send(
                            "You don't have the permission to execute this command.",
                            ephemeral=True
                        )
                    return
            else:
                raise TypeError("require_permission decorator expected Interaction or Context")
            return await func(Interaction, *args, **kwargs)
        return wrapper
    return decorator
