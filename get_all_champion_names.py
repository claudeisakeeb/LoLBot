import requests
import json

all_champion_names = {}
version = requests.get("https://ddragon.leagueoflegends.com/api/versions.json").json()[0]
all_champions = requests.get(f"http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json").json()["data"]
for champion in all_champions.keys():
    all_champion_names[champion.lower()] = champion

with open("all_champion_names.json", "w") as f:
    json.dump(all_champion_names, f)
    print("Successfully generated all champion names.")