import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# commands
from commands import buy
from commands import sell

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    buy.setup(bot)
    sell.setup(bot)
    await bot.tree.sync()

bot.run(os.getenv('TOKEN'))