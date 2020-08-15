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
    embed_title, img_url, quote = lol.getChampionQuote(args)
    if embed_title == 404:
        await ctx.send("Please enter a valid champion name (no apostrophes)")
    else:
        embed = discord.Embed(
            title = embed_title,
            description = f"**{quote}**"
        )
        embed.set_image(url = img_url)
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
async def splash(ctx, *, args):
    embed_title, image_url = lol.getChampionSkin(args)
    if image_url == False:
        await ctx.send("Please enter a valid skin")
    else:
        embed = discord.Embed(
            title = embed_title
        )
        embed.set_image(url = image_url)
        await ctx.send(embed = embed)


client.run(DISCORD_API_KEY)