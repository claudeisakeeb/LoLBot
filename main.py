import discord
import random
from discord.ext import commands
import lol
import requests
import json
import asyncio

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
    if embed_title == 404:
        await ctx.send("Please enter a valid skin")
    else:
        embed = discord.Embed(
            title = embed_title
        )
        embed.set_image(url = image_url)
        await ctx.send(embed = embed)

@client.command()
async def trivia(ctx, *args):
    if len(args) != 2:
        await ctx.send("Please enter the command in the form \'/trivia [item/spell] [number of rounds]")
    else:
        quizType, quizLength = args
        if quizType not in ("item", "spell"):
            await ctx.send("Please enter a valid quiz type (item/spell)")
            return
        elif not quizLength.isdigit() or int(quizLength) <= 0 or int(quizLength) > 15:
            await ctx.send("Please enter a valid integer for the trivia length [0-15]")
            return
        correct = 0

        def check(author):
            def inner_check(message):
                return message.author == author and message.content.lower() == quizWord.lower()
            return inner_check
            
        for i in range(1, int(quizLength)+1):
            item, img_url = lol.generateRandomItem()
            quizWord = item
            print(quizWord)
            embed = discord.Embed(title = f"{i}.")
            embed.set_image(url = img_url)
            await ctx.send(embed = embed)
            try:
                attempt = await client.wait_for("message", check = check(ctx.author), timeout = 5)
                if attempt:
                    await ctx.send("Correct!")
                    correct +=1
            except asyncio.TimeoutError:
                continue
        embed = discord.Embed(
            title = f"Score Report for {ctx.author}'s quiz",
        )
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.add_field(name="Correct Questions", value = correct, inline = False)
        embed.add_field(name="Total Questions", value = quizLength, inline = False)
        embed.add_field(name="Total score", value = f"{correct}/{quizLength} = {correct/int(quizLength) * 100}%")
        await ctx.send(embed = embed)

@client.command()
async def pfp(ctx, *args):
    if len(args) != 1:
        await ctx.send("Please format the command as '/pfp [valid user mention]'")
        return
    target = client.get_user(int(args[0][2:len(args[0])-1]))
    if target != None:
        embed = discord.Embed(
            title = f"{target}'s profile picture:"
        )
        embed.set_image(url=target.avatar_url)
        await ctx.send(embed = embed)
    else:
        await ctx.send("Please format the command as '/pfp [valid user mention]'")

client.run(DISCORD_API_KEY)