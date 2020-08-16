import requests
import json

version = requests.get("https://ddragon.leagueoflegends.com/api/versions.json").json()[0]
all_champion_spells = {}
all_champions = requests.get(f"http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json").json()["data"]
for c in all_champions:
    all_champion_spells[c] = []
    data = requests.get(f"http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion/{c}.json").json()["data"][c]
    spells = data["spells"]
    for spell in spells:
        all_champion_spells[c].append(spell["image"]["full"])
    passive = data["passive"]
    all_champion_spells[c].append(passive["image"]["full"])

with open("all_champion_spells.json", "w") as f:
    json.dump(all_champion_spells, f)
    print("Successfully generated all champion spells.")