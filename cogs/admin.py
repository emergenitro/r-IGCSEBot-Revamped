import nextcord as discord
from nextcord.ext import commands

class Admin(commands.Cog):
	def __init__(self, client):
		self.client = client

	@discord.slash_command(name='reload', description='Reloads all cogs')
	@commands.is_owner()
	async def reload_cogs(self, ctx):
		"""Reloads all cogs except the Admin cog"""
		for cog in list(self.client.cogs):
			if cog != 'Admin':
				print(f'Reloading {cog.lower()}')
				self.client.reload_extension(f"cogs.{cog.lower()}")
		await ctx.response.send_message('All cogs reloaded except Admin.')

	@discord.slash_command(name='unload', description='Unloads a specific cog')
	@commands.is_owner()
	async def unload_cog(self, ctx, cog: str):
		self.client.unload_extension(f"cogs.{cog.lower()}")
		await ctx.response.send_message(f'{cog} unloaded.')
	
	@discord.slash_command(name='load', description='Loads a specific cog')
	@commands.is_owner()
	async def load_cog(self, ctx, cog: str):
		self.client.load_extension(f"cogs.{cog.lower()}")
		await ctx.response.send_message(f'{cog} loaded.')
  
	@discord.slash_command(name='listcogs', description='Lists all cogs')
	@commands.is_owner()
	async def list_cogs(self, ctx):
		cogs = list(self.client.cogs)
		await ctx.response.send_message(f'Loaded cogs: {", ".join(cogs)}')



def setup(client):
	client.add_cog(Admin(client))
