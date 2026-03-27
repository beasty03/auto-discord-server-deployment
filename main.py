import discord
from discord.ext import commands
import asyncio
import os
from setup_variables import SETUPBOT_TOKEN, GUILD_ID, COGS_DIR

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

async def load_cogs():
    for filename in os.listdir(COGS_DIR):
        if filename.endswith('.py') and not filename.startswith('_'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f"Loaded cog: cogs.{filename[:-3]}")
            except Exception as e:
                print(f"Failed to load cogs.{filename[:-3]}: {e}")

@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user.name} (id={bot.user.id})")
    
    guild = discord.Object(id=GUILD_ID)
    try:
        synced = await bot.tree.sync(guild=guild)
        print(f"Commands synced to guild {GUILD_ID}")
        print(f"Synced commands: {[cmd.name for cmd in synced]}")
        
        all_commands = bot.tree.get_commands(guild=guild)
        print(f"After sync, app commands: {[cmd.name for cmd in all_commands]}")
        
        # DEBUG: Print all loaded cogs and their commands
        print("\n=== DEBUG INFO ===")
        for cog_name, cog in bot.cogs.items():
            print(f"Cog: {cog_name}")
            for cmd in cog.get_app_commands():
                print(f"  - Command: {cmd.name}")
        print("==================\n")
        
    except Exception as e:
        print(f"Failed to sync commands: {e}")

async def main():
    async with bot:
        await load_cogs()  # Load cogs BEFORE starting the bot
        await bot.start(SETUPBOT_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())