import discord
import random
from discord.ext import commands
import lol
import requests
import json
import asyncio
import time
from discord.ext import tasks

with open("token.txt", "r") as keys:
    sample_text = keys.readline()
    DISCORD_API_KEY = keys.readline()

client = commands.Bot(command_prefix = "/")

#*******************GENERAL COMMANDS/EVENTS***************************
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
async def pfp(ctx, *args):
    if len(args) != 1:
        await ctx.send("Please format the command as '/pfp [VALID USER MENTION]'")
        return
    target = client.get_user(int(args[0][2:len(args[0])-1]))
    if target != None:
        embed = discord.Embed(
            title = f"{target}'s profile picture:"
        )
        embed.set_image(url=target.avatar_url)
        await ctx.send(embed = embed)
    else:
        await ctx.send("Please format the command as '/pfp [VALID USER MENTION]'")

@client.command()
async def hecarim(ctx):
    responses = [
        "*clop clop*",
        "*neighs*",
        "*glares menacingly*"
    ]
    await ctx.send(random.choice(responses))

client.remove_command("help")
@client.command()
async def help(ctx):
    with open("help.txt", "r") as f:
        await ctx.author.send("".join(f.readlines()))
    await ctx.send(f"{ctx.author.mention} DM sent! :100:")

@client.command()
async def role(ctx, *, args):
    roles ={
        "top": "Top",
        "jungle": "Jungle",
        "jg": "Jungle",
        "mid": "Mid",
        "bot": "Bot",
        "adc": "Bot",
        "supp": "Supp",
        "support": "Supp"

    }
    if len(args) != 1 or args[0].lower() not in roles:
        await ctx.send(f"{ctx.user.mention}, Invalid role.")
    else:
        to_add = discord.utils.get(ctx.member.guild.roles, name = roles[args[0].lower()])
        await ctx.member.add_roles(to_add)

@client.event
async def on_ready():
    print("Bot is ready")

#*******************LEAGUE OF LEGENDS RELATED COMMANDS/EVENTS***************************
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
    if len(args) not in (2, 3):
        await ctx.send("Please enter the command in the form \'/trivia [ITEM/SPELL] [NUMBER OF ROUNDS (1-15)] [*OPTIONAL* TIME LIMIT PER QUESTION (1-15)]")
    else:
        if len(args) == 2:
            quizType, quizLength = args
            timeLimit = 10
        else:
            quizType, quizLength, timeLimit = args
        if quizType not in ("item", "champion"):
            await ctx.send("Please enter a valid quiz type (item/champion)")
            return
        elif not quizLength.isdigit() or int(quizLength) < 1 or int(quizLength) > 15:
            await ctx.send("Please enter a valid integer for the trivia length (1-15)")
            return
        elif len(args) == 3 and (not timeLimit.isdigit() or int(timeLimit) < 1 or int(timeLimit) > 15):
            await ctx.send("Please enter a valid integer for the question time limit (1-15)")

        def check(author):
            def inner_check(message):
                return message.author == author and message.content.lower().replace("'", "") == quizWord.lower()
            return inner_check
        
        @tasks.loop(seconds = 1, count = timeLimit)
        async def update_embed():
            nonlocal tempTimeLimit
            tempTimeLimit -= 1
            await original.edit(content = f"Time left: {tempTimeLimit}")

        functions = {
            "item": lol.generateRandomItem,
            "champion": lol.generateRandomChampionSpell
        }
        intros = {
            "item": "Given an item's store icon, guess the item's name!",
            "champion": "Given a champion's passive or spell, guess the champion!"
        }
        await ctx.send(intros[quizType])
        quizLength, timeLimit = int(quizLength), int(timeLimit)
        correct = 0
        for i in range(1, quizLength+1):
            item, img_url = functions[quizType]()
            quizWord = item
            print(quizWord)
            embed = discord.Embed(title = f"Question {i}")
            embed.set_image(url = img_url)
            await ctx.send(embed = embed)
            original = await ctx.send(f"Time left: {timeLimit}")
            try:
                tempTimeLimit = timeLimit
                update_embed.start()
                await client.wait_for("message", check = check(ctx.author), timeout = timeLimit)
                update_embed.cancel()
                await original.edit(content = f"Correct! The answer is '{quizWord}'")
                correct +=1
            except asyncio.TimeoutError:
                await original.edit(content = f"Times up! The correct answer was '{quizWord}'")
                update_embed.cancel()
                continue
        embed = discord.Embed(
            title = f"Score Report for {ctx.author}'s quiz"
        )
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.add_field(name="Correct Questions", value = correct, inline = False)
        embed.add_field(name="Total Questions", value = quizLength, inline = False)
        embed.add_field(name="Total score", value = f"{correct}/{quizLength} = {correct/int(quizLength) * 100}%")
        await ctx.send(embed = embed)

@client.command()
async def summoner(ctx, *, args):
    if len(args) < 2:
        await ctx.send("Please format your command as '/summoner [REGION (BR / EUN / EUW / JP / KR / LA / NA / OCE / RU / TR)] [SUMMONER NAME]")
    else:
        result = lol.getSummonerInfo(args)
        if result == "404region":
            await ctx.send("Region not found. This bot supports: BR / EUN / EUW / JP / KR / LA / NA / OCE / RU / TR. Please try again.")
        elif result == "404summonerEntry":
            await ctx.send("Please enter a summoner name.")
        elif result == "404summoner":
            await ctx.send("Summoner not found in specified region. Please try again.")
        else:
            await ctx.send(embed = result)

client.run(DISCORD_API_KEY)