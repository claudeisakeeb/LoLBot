import requests
import json

all_champions_by_id = {}
version = requests.get("https://ddragon.leagueoflegends.com/api/versions.json").json()[0]
all_champions = requests.get(f"http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json").json()["data"]
for champion in all_champions.keys():
    all_champions_by_id[int(all_champions[champion]["key"])] = champion

with open("all_champions_by_id.json", "w") as f:
    json.dump(all_champions_by_id, f)
    print("Successfully generated all champions by id.")