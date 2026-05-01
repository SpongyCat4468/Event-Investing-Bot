import discord
from discord.ext import commands as cmd
import os
from dotenv import load_dotenv

import commands
import help


load_dotenv()

intents = discord.Intents.all()
bot = cmd.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    commands.setup(bot)
    help.setup(bot)
    await bot.tree.sync()

bot.run(os.getenv('TOKEN'))