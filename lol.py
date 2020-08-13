import requests

def getSummonerInfo(region, name):
    url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}?api_key=RGAPI-8ee22b71-1933-4ba1-8c17-cf8c92ca2324"
    response = requests.get(url)
    print(response.json())

getSummonerInfo("na1", "ritobalanceteamx")