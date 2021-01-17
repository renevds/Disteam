import requests
from bs4 import BeautifulSoup
#import gamefinderbot

class User(object):
    def __init__(self, steamID):
        self.steamID = steamID
        self.steamProfileLink = "https://steamcommunity.com/profiles/{}".format(steamID)
        self.steamName = self.getSteamName()
        self.steamLevel = self.getSteamLevel()
        self.discordID = ""

    def getSteamName(self):
        html = requests.get(self.steamProfileLink).text
        print(self.steamProfileLink)
        soup = BeautifulSoup(html, "html.parser")
        spans = soup.find_all('span', {'class': 'actual_persona_name'})
        name = spans[0].get_text()
        if len(spans) == 0:
            return "unknown"
        return name

    def getSteamLevel(self):
        html = requests.get(self.steamProfileLink).text
        print(self.steamProfileLink)
        soup = BeautifulSoup(html, "html.parser")
        spans = soup.find_all('span', {'class': 'friendPlayerLevelNum'})
        lvl = spans[0].get_text()
        if len(spans) == 0:
            return 0
        return int(lvl)

    def update(self):
        self.steamName = self.getSteamName()

    def __lt__(self, given):
        if self.steamLevel > given.steamLevel:
            return True
        elif self.steamLevel == given.steamLevel:
            return self.steamName > given.steamName
        else:
            return False

def generateUsers(games):
    users = []
    IDs = []
    for i in games:
        IDs += i.steamIDs
    IDs = set(IDs)
    for i in IDs:
        users.append(User(i))
    #gamefinderbot.writeUsers(users)
    print("test in fun" + str(users))

#generateUsers(gamefinderbot.loadGames())
