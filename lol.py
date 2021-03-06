import requests
import json
import random
import discord
import os
import token
import re

try:
    LOL_API_KEY = os.environ["LEAGUE_API_KEY"]
except KeyError:
    with open("token.txt") as f:
        LOL_API_KEY = f.readline()

def getChampionSkin(args):
    desired_skin = "".join(list(args)).lower().replace("'", "").replace("/", "")
    with open("all_champion_skins.json", "r") as f:
        all_skins = json.load(f)
        if desired_skin in all_skins:
            champion, id, ogn, skinID = all_skins[desired_skin]
            embed = discord.Embed(
                title = f"{ogn} - #{skinID}"
            )
            embed.set_image(url = f"http://ddragon.leagueoflegends.com/cdn/img/champion/splash/{champion}_{id}.jpg")
            return embed
        else:
            return 404

def generateRandomItem():
    version = requests.get("https://ddragon.leagueoflegends.com/api/versions.json").json()[0]
    items = requests.get(f"http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/item.json").json()["data"]
    item = random.choice(list(items.keys()))
    img_url = f"http://ddragon.leagueoflegends.com/cdn/{version}/img/item/{item}.png"
    return items[item]["name"], img_url

def generateRandomChampionSpell():
    version = requests.get("https://ddragon.leagueoflegends.com/api/versions.json").json()[0]
    with open("all_champion_spells.json", "r") as f:
        data = json.load(f)
        champion = random.choice(list(data.keys()))
        spell_index = random.choice([0,1,2,3,4])
        if spell_index == 4:
            img_url = f"http://ddragon.leagueoflegends.com/cdn/{version}/img/passive/{data[champion][spell_index]}"
        else:
            img_url = f"http://ddragon.leagueoflegends.com/cdn/{version}/img/spell/{data[champion][spell_index]}"

    champion_output = [champion[0]]
    for c in champion[1:]:
        if c == c.upper():
            champion_output.append(" ")
        champion_output.append(c)

    return "".join(champion_output), img_url

def getSummonerInfo(args):
    version = requests.get("https://ddragon.leagueoflegends.com/api/versions.json").json()[0]
    regions = {
         "br": "BR1",
         "eun": "EUN1",
         "euw": "EUW1",
         "jp": "JP1",
         "kr": "KR",
         "las": "LA2",
         "lan": "LA1",
         "na": "NA1",
         "oce": "OC1",
         "ru": "RU",
         "tr": "TR1"
    }
    args = args.lower().split()
    if not args or args[0] not in regions:
        return "404region"
    elif len(args) == 1:
        return "404summonerEntry"
    region = args[0]
    summoner = "".join(args[1:])
    url = f"https://{regions[region]}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner}?api_key={LOL_API_KEY}"
    data = requests.get(url).json()
    if "status" in data: 
        return "404summoner"
    pfp_url = f"http://ddragon.leagueoflegends.com/cdn/{version}/img/profileicon/{data['profileIconId']}.png"
    all_ranked_info = requests.get(f"https://{regions[region]}.api.riotgames.com/lol/league/v4/entries/by-summoner/{data['id']}?api_key={LOL_API_KEY}").json()
    all_champion_info = requests.get(f"https://{regions[region]}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{data['id']}?api_key={LOL_API_KEY}").json()
    for ranked in all_ranked_info:
        if ranked["queueType"] == "RANKED_SOLO_5x5":
            ranked_info = ranked
            break
    else:
        ranked_info = "None"
    embed = discord.Embed(
        title = f"{data['name']} - {region.upper()}"
    )
    embed.set_thumbnail(url=pfp_url)
    embed.add_field(name="Rank:", value= f"{ranked_info['tier']} {ranked_info['rank']} - {ranked_info['leaguePoints']} LP" if ranked_info != "None" else ranked_info)
    embed.add_field(name="Winrate:", value = f"W: {ranked_info['wins']} L: {ranked_info['losses']} ({round(ranked_info['wins']/(ranked_info['wins'] + ranked_info['losses']) * 100)}%)" if ranked_info != "None" else ranked_info, inline = False)
    top_champions = ""
    with open("all_champions_by_id.json", "r") as f:
        data = json.load(f)
        for i in range(min(5, len(all_champion_info))):
            champion = data[str(all_champion_info[i]["championId"])]
            level = all_champion_info[i]["championLevel"]
            points = all_champion_info[i]["championPoints"]
            top_champions += f"{i+1}. {champion} - Level {level} - {points} points\n"
    embed.add_field(name="Top Played Champions: ", value=top_champions if top_champions else "None")
    embed.add_field(name="For a more comprehensive overview:", value=f"https://{region}.op.gg/summoner/userName={summoner}", inline = False)
    return embed

def getChampionStats(args):

    spells = {
        0: "Q",
        1: "W",
        2: "E",
        3: "R"
    }

    args = "".join(list(args)).lower().replace("'", "")
    version = requests.get("https://ddragon.leagueoflegends.com/api/versions.json").json()[0]
    with open("all_champion_names.json", "r") as f:
        data = json.load(f)
        if args not in data:
            return "404champion"
    champion = data[args]
    champion_info = requests.get(f"http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion/{champion}.json").json()["data"][champion]
    embed = discord.Embed(
        title = champion,
        description=f"**{champion_info['title']}**",
        colour=discord.Colour.blurple()
    )
    embed.set_thumbnail(url=f"http://ddragon.leagueoflegends.com/cdn/{version}/img/champion/{champion}.png")
    embed.set_image(url=f"http://ddragon.leagueoflegends.com/cdn/img/champion/splash/{champion}_0.jpg")
    champion_spells = champion_info["spells"]
    for i in range(len(champion_spells)):
        name=f"{spells[i]} - {champion_spells[i]['name']}"
        value=f"{re.sub(r'<.*>', ' ', champion_spells[i]['description'])}\n\nCooldown: {champion_spells[i]['cooldownBurn']}"
        embed.add_field(name=name, value=value, inline=False)
    embed.add_field(name="For a more comprehensive overview of champions:", value=f"https://na.leagueoflegends.com/en-us/champions//")
    return embed

getChampionStats(("yone"))
    