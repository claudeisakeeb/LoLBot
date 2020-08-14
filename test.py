import json

with open("all_champion_quotes.json") as json_file:
    data = json.load(json_file)
    for key in data.keys():
        temp = data[key]
        del data[key]
        data[key.lower()] = temp
    for key in data.keys():
        print(key)
