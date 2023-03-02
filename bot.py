import os
import discord

from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

global CLIENT

bot = discord.Bot()

#Bot commands
@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.slash_command(guild_ids=[os.getenv("GUILD_ID")])
async def hello(ctx):
    card_data = await get_card_data()
    await ctx.respond(card_data)


async def get_card_data(tokenId=10822):
    global CLIENT

    query = format_query()

    params = {"tokenId": tokenId}
    result = await CLIENT.execute_async(query, variable_values=params)

    return format_result(result)

def format_query():
    return gql(
        """
        query ($tokenId: String!){
            getParallelAssets(tokenIds: [$tokenId]) {
                items {
                    gameData {
                        attack
                        cost
                        health
                    }
                    name
                    }
                }
            }
        """
    )

def format_result(result):
    name = result["getParallelAssets"]["items"][0]["name"]
    cost = result["getParallelAssets"]["items"][0]["gameData"]["cost"]
    attack = result["getParallelAssets"]["items"][0]["gameData"]["attack"]
    health = result["getParallelAssets"]["items"][0]["gameData"]["health"]

    return f'''Name: {name}\nCost: {cost}\nAttack: {attack}\nHealth: {health}'''

def main():
    global CLIENT
    
    # Select your transport with a defined url endpoint
    transport = AIOHTTPTransport(url="https://api.defined.fi", headers={'Content-Type': 'application/json', 'x-api-key': os.getenv("DEFINED_API_KEY")})

    # Create a GraphQL client using the defined transport
    CLIENT = Client(transport=transport, fetch_schema_from_transport=True)

    bot.run(os.getenv("DISCORD_TOKEN"))

main()