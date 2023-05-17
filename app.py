import nextcord as discord
from nextcord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TOKEN")
dbURL = os.getenv("DB")

intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix="!", intents=intents)

serverTest = 1065277336548814928

@client.event
async def on_ready():
	print("Bot is ready")


modules = []

for file in os.listdir("./cogs"):
	if file.endswith(".py"):
		print(f"Loading {file}")
		modules.append("cogs." + file[:-3].lower())

if __name__ == "__main__":
    for module in modules:
        try:
            client.load_extension(f"{module}")
        except Exception as e:
            print(f'Error loading {module}: {e}')


client.run(token)