import requests
import json

#Gets all champion skins in the current version of data dragon and puts them in 'all_champion_skins.json'

with open("all_champion_skins.json", "r") as f:
    champion_skin_dict = {}
    version = requests.get("https://ddragon.leagueoflegends.com/api/versions.json").json()[0]
    all_champions = requests.get(f"http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json").json()["data"]
    for champion in all_champions:
        champion_skins = requests.get(f"http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion/{champion}.json").json()["data"][champion]["skins"]
        for skin in champion_skins:
            key = champion.lower().replace(" ", "") if skin["name"] == "default" else skin["name"].lower().replace(" ", "")
            champion_skin_dict[key] = [champion, skin["num"], f"Classic {champion}" if skin["name"] == "default" else skin["name"], skin["id"]]

with open("all_champion_skins.json", "w") as f:
    json.dump(champion_skin_dict, f)
    print("Successfully generated all champion skins.")