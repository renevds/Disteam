import requests
from bs4 import BeautifulSoup
def getNames():
    html = open("html.html", "r").read()
    print(html)
    soup = BeautifulSoup(html, "html.parser")
    spans = soup.find_all('th', {'class': 'd_gn d_ich', 'scope':"row"})
    spans = [i.get_text() for i in spans]
    names = []
    for i in spans:
        i.replace(" ", "")
        i = i.split(",")
        names.append((i[0], i[1]))
    print(names)
    return names
