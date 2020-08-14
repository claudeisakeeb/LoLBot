import requests
import json
import random

with open("keys.txt", "r") as keys:
    LOL_API_KEY = keys.readline()

def getSummonerInfo(region, name):
    url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}?api_key={LOL_API_KEY}"
    response = requests.get(url)
    print(response.json())

def getChampionQuote(ch = None):
    corrected = {
        "leesin": "LeeSin",
        "drmundo": "DrMundo",
        "masteryi": "MasterYi",
        "missfortune": "MissFortune",
        "reksai": "RekSai",
        "monkeyking": "MonkeyKing",
        "aurelionsol": "AurelionSol",
        "tahmkench": "TahmKench"
    }
    with open("all_champion_quotes.json") as json_file:
        data = json.load(json_file)
        champions = [c for c in data.keys()]
        if ch != None:
            if ch.lower() == "wukong":
                champion = "MonkeyKing"
            else:
                for key in data.keys():
                    if ch.lower() == key.lower():
                        champion = key
                        break
                else:
                    return "Please enter a valid champion name (no spaces or quotes).", False
        else:
            champion = random.choice(champions)
        champion_quotes = data[champion]["quotes"]
        section = random.choice(list(champion_quotes.keys()))
        interaction = random.choice(list(champion_quotes[section].keys()))
    img_key = champion[0].upper() + champion[1:].lower() if champion.lower() not in corrected else corrected[champion.lower()]
    return f"{champion_quotes[section][interaction]}", img_key
