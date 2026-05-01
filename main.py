import discord
from discord.ext import commands as cmd
import os
from dotenv import load_dotenv

import commands
import help
import admin_commands

import sqlite3

DB_PATH = "data.db"
db = sqlite3.connect(DB_PATH)
cursor = db.cursor()

load_dotenv()

intents = discord.Intents.all()
bot = cmd.Bot(command_prefix='!', intents=intents)

cursor.executescript("""
    CREATE TABLE IF NOT EXISTS user_permissions (
        guild_id   INTEGER NOT NULL,
        user_id    INTEGER NOT NULL,
        permission TEXT    NOT NULL,
        PRIMARY KEY (guild_id, user_id, permission)
    );
                     
    CREATE TABLE IF NOT EXISTS game_state (
        guild_id   INTEGER NOT NULL PRIMARY KEY,
        is_running INTEGER NOT NULL DEFAULT 0
    );
""")

db.commit()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    commands.setup(bot)
    help.setup(bot)
    admin_commands.setup(bot)
    await bot.tree.sync()

bot.run(os.getenv('TOKEN'))