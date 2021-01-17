import requests
import re

class Game:
    amount = 0

    def __init__(self, gameid, gamename, steamids):
        Game.amount += 1
        self.gameID = gameid
        self.gameName = gamename
        self.steamIDs = steamids
        self.reviews = int(self.getReviews())

    def getOwners(self):
        return len(self.steamIDs)

    def getReviews(self):
        gameID = self.gameID
        url = "https://store.steampowered.com/app/{}".format(gameID)
        print(url)
        html = requests.get(url).text
        htmllines = html.split("\n")
        results = []
        for i in htmllines:
            results += re.findall(r"(<span>\()(\d+(,\d{3})*(\.\d+)?)( reviews\)<\/span>)", i)
        numbers = []
        for i in results:
            numbers.append(i[1].replace(",", ""))
        if len(numbers) == 0:
            print(0)
            return 0
        print(max(numbers))
        return max(numbers)

    def __lt__(self, given):
        if self.getOwners() > given.getOwners():
            return True
        elif self.getOwners() == given.getOwners():
            return self.reviews > given.reviews
        else:
            return False

    def update(self):
        self.reviews = self.getReviews()






