import nextcord as discord
from nextcord.ext import commands
from pymongo import MongoClient
import plotly.express as px
import io
import pandas as pd
import os

dbURL = os.getenv("DB")

class Reputation(commands.Cog):
	def __init__(self, client):
		self.client = client
		self.db = MongoClient(dbURL).test

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.guild:
			content = message.content.lower()
			if "thank" in content and message.mentions:
				db = self.db[str(message.guild.id)]
				for user in message.mentions:
					if user != message.author:
						db.update_one(
							{"id": user.id},
							{
								"$inc": {"rep": 1},
								"$push": {"history": {"date": message.created_at, "rep": 1}}
							},
							upsert=True
						)
						embed = discord.Embed(description=f"Gave +1 rep to {user.display_name}")
						await message.channel.send(embed=embed)

	 

	@discord.slash_command(name="repgraph", description="Displays a user's reputation over time")
	async def repgraph(self, ctx: discord.Interaction, user: discord.User):
		await ctx.response.defer(ephemeral=False)
		await ctx.edit_original_message(content="Loading...")
		data = self.db[str(ctx.guild_id)].find_one({"id": user.id})
		if not data or "history" not in data:
			await ctx.edit_original_message(content=f"No reputation data found for {user.display_name}")
			return

		df = pd.DataFrame(data["history"])
		df["rep"] = df["rep"].cumsum()
		fig = px.line(df, x="date", y="rep", title=f"{user.display_name}'s Reputation Over Time")
		fig.update_layout(xaxis_title="Date", yaxis_title="Reputation")

		buf = io.BytesIO()
		fig.write_image(buf, format="png")
		buf.seek(0)
		file = discord.File(buf, filename="repgraph.png")

		embed = discord.Embed(title=f"{user.display_name}'s Reputation Over Time")
		embed.set_image(url="attachment://repgraph.png")
		await ctx.edit_original_message(content=None, embed=embed, file=file)


def setup(client):
	client.add_cog(Reputation(client))