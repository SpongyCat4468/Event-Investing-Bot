import datetime
import discord
import os
from dotenv import load_dotenv

load_dotenv()

# Terminal colors (for console output)
RESET   = "\033[0m"
CYAN    = "\033[96m"
GREEN   = "\033[92m"
BLUE    = "\033[94m"
YELLOW  = "\033[93m"
MAGENTA = "\033[95m"
RED     = "\033[91m"


def now_str() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# --- Log Functions ---
def log(text):
    print(f"{CYAN}{now_str()}{RESET} {GREEN}[LOG]{RESET} {text}")


async def log_command(interaction: discord.Interaction):
    print(
        f"{CYAN}{now_str()}{RESET} {BLUE}[COMMAND]{RESET} "
        f"/{interaction.command.name} used by @{interaction.user} in #{interaction.channel}, {interaction.guild.name}"
    )

async def log_error(error):
    print(f"{CYAN}{now_str()}{RESET} {RED}[ERROR]{RESET} {error}")


def log_debug(text):
    print(f"{CYAN}{now_str()}{RESET} {MAGENTA}[DEBUG]{RESET} {text}")