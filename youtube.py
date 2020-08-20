import requests
import json
import discord

with open("token.txt", "r") as f:
    sample_text1 = f.readline()
    sample_text2 = f.readline()
    YOUTUBE_API_KEY = f.readline()

def getYoutubeVideos(args):

    def generateQuery(args):
        return  "%20".join(args)

    args = list(args)
    maxResults = 3
    if args and args[-1].isdigit() and 1 <= int(args[-1]) <= 5:
        maxResults = args[-1]
        args = args[:len(args)-1]
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=25&q={generateQuery(args)}&maxResults={maxResults}&type=video&key={YOUTUBE_API_KEY}"
    data = requests.get(url).json()["items"]
    embed = discord.Embed(
        title=f"Top {maxResults} results for '{' '.join(args)}':",
        colour=discord.Colour.red()
    )
    for item in data:
        print(item["id"])
        description = f"https://youtube.com/watch?v={item['id']['videoId']}\n"
        to_add = item["snippet"]["description"]
        description += f"{to_add[:min(len(to_add), 80)]}..."
        embed.add_field(name=item["snippet"]["title"],value=description, inline=False)
    if len(data) > 0:
        embed.set_image(url=data[0]["snippet"]["thumbnails"]["high"]["url"])
    return embed

#request = client.search().list()
#repsonse = request.execute()