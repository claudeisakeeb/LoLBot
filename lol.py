import requests

def getSummonerInfo(region, name):
    url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}?api_key=XXX"
    response = requests.get(url)
    print(response.json())

getSummonerInfo("na1", "ritobalanceteamx")