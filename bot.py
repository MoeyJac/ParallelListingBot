import os
import discord

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.slash_command(guild_ids=[os.getenv("GUILD_ID")])
async def hello(ctx):
    await ctx.respond("Hello Guy!")

bot.run(os.getenv("DISCORD_TOKEN"))
