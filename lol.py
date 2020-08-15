import requests
import json
import random

with open("keys.txt", "r") as keys:
    LOL_API_KEY = keys.readline()

def getSummonerInfo(region, name):
    url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}?api_key={LOL_API_KEY}"
    response = requests.get(url)
    print(response.json())

def getChampionQuote(args):
    args = "".join(list(args))
    version = requests.get("https://ddragon.leagueoflegends.com/api/versions.json").json()[0]
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
        if args != "":
            if args in data.keys():
                champion = args
                quote = random.choice(data[champion])
            else:
                return 404, False, False
        else:
            champion = random.choice(list(c for c in data.keys()))
            quote = random.choice(data[champion])

    img_key = champion[0].upper() + champion[1:].lower() if champion not in corrected else corrected[champion]
    champion_title = requests.get(f"http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion/{img_key}.json").json()["data"][img_key]["title"]
    embed_title = f"{img_key} - {champion_title}"
    img_url = f"http://ddragon.leagueoflegends.com/cdn/{version}/img/champion/{img_key}.png"

    return embed_title, img_url, quote

def getChampionSkin(args):
    desired_skin = args.lower().replace(" ", "")
    with open("all_champion_skins.json", "r") as f:
        all_skins = json.load(f)
        if desired_skin in all_skins:
            champion, id, ogn, skinID = all_skins[desired_skin]
            title = f"{ogn} - #{skinID}"
            image_url = f"http://ddragon.leagueoflegends.com/cdn/img/champion/splash/{champion}_{id}.jpg"
            return title, image_url
        else:
            return 404, False
