import discord
import random
from discord.ext import commands

client = commands.Bot(command_prefix = "/")

@client.event
async def on_ready():
    print("Bot is ready")

@client.command()
async def motd(ctx):
    quotes = ["Pain",
                    ]
    await ctx.send(f"Message of the day: f{random.choice(quotes)}")
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


client.run("NzQyNjA3ODczMDUzNTU2ODE4.XzIleQ.5VYj1VFgPbK_mEK2wQRMna-_fFY")