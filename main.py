import discord
from discord.ext import commands as cmd
import os
from dotenv import load_dotenv

import user_commands
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
        user_id    INTEGER NOT NULL,
        permission TEXT    NOT NULL,
        PRIMARY KEY (user_id, permission)
    );
                     
    CREATE TABLE IF NOT EXISTS game_state (
    id INTEGER PRIMARY KEY DEFAULT 1,
    is_running INTEGER NOT NULL DEFAULT 0,
    CHECK (id = 1)  -- enforces only one row ever exists
)
""")

db.commit()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    user_commands.setup(bot)
    help.setup(bot)
    admin_commands.setup(bot)
    await bot.tree.sync()

bot.run(os.getenv('TOKEN'))