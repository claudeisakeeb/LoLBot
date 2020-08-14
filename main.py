import discord
import random
from discord.ext import commands
import lol
import requests
import json

with open("keys.txt", "r") as keys:
    sample_text = keys.readline()
    DISCORD_API_KEY = keys.readline()

client = commands.Bot(command_prefix = "/")

@client.event
async def on_ready():
    print("Bot is ready")

@client.command()
async def quote(ctx, *args):
    if len(args) not in (0,1):
        await ctx.send("Please enter one or zero champions (no spaces or quotes)")
    elif len(args) == 1:
        message, img_key = lol.getChampionQuote(args[0])
    else:
        message, img_key = lol.getChampionQuote()
    if img_key == False: 
        await ctx.send(message)
        return
    champion_title = requests.get(f"http://ddragon.leagueoflegends.com/cdn/10.16.1/data/en_US/champion/{img_key}.json").json()["data"][img_key]["title"]
    embed = discord.Embed(
        title = f"{img_key} - {champion_title}",
        description = message
    )
    embed.set_image(url = f"http://ddragon.leagueoflegends.com/cdn/10.16.1/img/champion/{img_key}.png")
    await ctx.send(embed=embed)

@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! {client.latency * 1000} ms")

@client.command(aliases = ["8ball"])
async def _8ball(ctx,*,question):
    responses = ["It is certain.",
                "It is decidedly so.",
                "Without a doubt.",
                "Yes - definitely.",
                "You may rely on it.",
                "As I see it, yes.",
                "Most likely.",
                "Outlook good.",
                "Yes.",
                "Signs point to yes.",
                "Reply hazy, try again.",
                "Ask again later.",
                "Better not tell you now.",
                "Cannot predict now.",
                "Concentrate and ask again.",
                "Don't count on it.",
                "My reply is no.",
                "My sources say no.",
                "Outlook not so good.",
                "Very doubtful.",
                "Pain."]
    await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")

@client.command()
async def img(ctx, *args):
    if len(args) != 1:
        await ctx.send("Please name 1 champion")
    else:
        pass


client.run(DISCORD_API_KEY)