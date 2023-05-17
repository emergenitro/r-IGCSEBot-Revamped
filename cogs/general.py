import nextcord as discord
from nextcord.ext import commands
from pymongo import MongoClient
import os

dbURL = os.getenv("DB")

class General(commands.Cog):
	def __init__(self, client):
		self.client = client
		self.db = MongoClient(dbURL).test

	@commands.Cog.listener()
	async def on_ready(self):
		for guild in self.client.guilds:
			collections = self.db.list_collection_names()
			if f"{guild.id}" not in collections:
				self.db.create_collection(f"{guild.id}")

	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		await db.create_collection(f"{guild.id}")

def setup(client):
	client.add_cog(General(client))