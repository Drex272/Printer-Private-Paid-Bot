
import io
import json
import random
import aiohttp
from discord.ext import tasks
import asyncio
from colorama import Fore
import discord
from discord.ext import commands
import jishaku
import os

os.system("cls")



intent = discord.Intents.all()
intent.presences = False


ownss = [936581929078239252 , 738067016644296814 , 975133587563221022]
clr = 0x2ecc71





client = commands.AutoShardedBot(
    command_prefix=["-"],
    case_insensitive=True,
    intents=intent,
    strip_after_prefix=True,
    owner_ids=ownss,
    allowed_mentions=discord.AllowedMentions(everyone=False, replied_user=False, roles=False),
    sync_commands_debug=True,
    sync_commands=True,
)
client.remove_command("help")

@client.event
async def on_ready():
    print(Fore.MAGENTA + "Success: client Is Connected To Discord")
    print(Fore.RED + "Loaded & Online!")
    print(Fore.BLUE + f"Logged in as: {client.user}" + Fore.RESET)



async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")



async def main():
    async with client:
        await load()
        await client.load_extension("jishaku")
        await client.start("")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"An error occurred: {e}")

