import discord
import difflib
import random
import getgames
import gamefinderbot_gameclass
from datetime import datetime
from shutil import copyfile
import leerlingenscraper
import gamefinderbot_userclass
import jsonpickle

prefix = "£"

client = discord.Client()
jsonpickle.set_encoder_options('json', sort_keys=True, indent=4)

@client.event
async def on_ready():
    print('steam game finder bot ready'.format(client))

@client.event
async def on_message(message):

    #add
    if message.content.startswith("{}add".format(prefix)):
        games = loadGames()
        arg = message.content.split(" ")[1]
        newGames = addOwnedGames(arg, games)
        if isinstance(newGames, str):
            await message.channel.send(newGames)
        else:
            games = newGames
        await printGames(games, message.channel)
        writeGames(games)

    #show
    if message.content.startswith("{}show".format(prefix)):
        print("show")
        arg = message.content.split(" ")[1]
        try:
            arg = int(arg)
        except:
            message.channel.send("argument not an integer")
        else:
            await printGames(loadGames(), message.channel, arg)

    # clear
    if message.content == "{}clear".format(prefix):
        print("clear")
        chamsg = await message.channel.history(limit=20000).flatten()
        for msg in chamsg:
            if msg.author == client.user:
                try:
                    await msg.delete()
                except:
                    None
            elif msg.content.startswith(prefix):
                try:
                    await msg.delete()
                except:
                    None

    # clearall
    if message.content == "{}clearall".format(prefix):
        print("delete")
        chamsg = await message.channel.history(limit=20000).flatten()
        for msg in chamsg:
            await msg.delete()

    #find
    if message.content.startswith("{}find".format(prefix)):
        games = loadGames()
        print("find")
        if len(message.content) < 6:
            message.channel.send("no argument given")
        else:
            key = message.content[6::]
            returned = getAllGameNames(games)
            match = find(key, returned)
            if len(match) == 0:
                await message.channel.send("no matches found")
            else:
                await message.channel.send(str(match[0]) + " has " + str(returned[match[0]].getOwners()) + " players")

    # update
    if message.content == "{}update".format(prefix):
        await message.channel.send("updating all numbers, this will take A WHILE")
        userIDs = []
        games = loadGames()
        for i in games:
            #i.update()
            userIDs += i.steamIDs
        counter = 0
        userIDs = set(userIDs)
        leng = len(userIDs)
        for i in userIDs:
            counter += 1
            await message.channel.send("updating user " + str(counter) + "of" + str(leng))
            addOwnedGames(i, games)
        users = loadUsers()
        #for i in users:
        #    i.update()
        writeUsers(loadUsers())
        writeGames(games)

    # suggest
    if message.content == "£suggest":
        value = 0
        games = loadGames()
        for i in games:
            if i.getOwners() > value:
                value = i.getOwners()
        gv = []
        for i in games:
            if i.getOwners() == value:
                gv.append(i)
        game = random.choice(gv)
        await message.channel.send("you should play: " + game.gameName + ", it has " + str(game.getOwners()) + " players")

    #say
    if message.content.startswith("{}say ".format(prefix)):
        await message.channel.send(message.content[4:])

    #backup
    if message.content == "{}backup".format(prefix):
        filename = "gamefinderbot_games_{}.txt".format(datetime.now().strftime("%Y%m%d-%H%M%S"))
        copyfile("gamefinderbot_games.txt", filename)
        await message.channel.send("**made backup at** {}".format(filename))

    #who
    if message.content.startswith("{}who".format(prefix)):
        users = loadUsers()
        games = loadGames()
        print("find")
        if len(message.content) < 6:
            message.channel.send("no argument given")
        else:
            key = message.content[6::]
            returned = getAllGameNames(games)
            matches = find(key, returned)
            if len(matches) == 0:
                await message.channel.send("no matches found")
            else:
                game = returned[matches[0]]
                owners = ""
                print(users)
                counter = 0
                for i in game.steamIDs:
                    print(i)
                    for j in users:
                        print("check")
                        print(j)
                        if j.steamID == i:
                            owners += " ,{}".format(j.steamName)
                            counter += 1
                print(owners)
                multiple = "s" if counter == 1 else ""
                await message.channel.send("*{}* own **{} {}**".format(owners[2:], multiple, game.gameName))

    #help
    if message.content == "{}help".format(prefix):
        await message.channel.send("**{}add** to add new steamID's".format(prefix))
        await message.channel.send("**{}show AMOUNT** to show AMOUNT top games".format(prefix))
        await message.channel.send("**{}find NAME** to find amount of owners of NAME".format(prefix))
        await message.channel.send("**{}update** to update all numbers (will take a while)".format(prefix))
        await message.channel.send("**{}say MESSAGE** to make the bot say MESSAGE".format(prefix))
        await message.channel.send("**{}backup** to make a backup".format(prefix))
        await message.channel.send("**{}suggest** to get a suggestion".format(prefix))
        await message.channel.send("**{}clear** to clear all bot messages/commands".format(prefix))
        await message.channel.send("**{}clearall** to clear all messages".format(prefix))
        await message.channel.send("**{}who NAME** to get names of players who own NAME".format(prefix))
        await message.channel.send("**{}levels AMOUNT** to show AMOUNT of players with highest level".format(prefix))
        await message.channel.send("**{}players** to show all current players".format(prefix))
        await message.channel.send("**{}connect STEAMID** connect discord account to steam account".format(prefix))
        await message.channel.send("**{}getdiscord STEAMNAME** shows discord nickname connected to STEAMNAME".format(prefix))
        await message.channel.send("**{}shrek** for instant orgasm".format(prefix))

    #names
    if message.content == "{}names".format(prefix):
        names = leerlingenscraper.getNames()
        print("test" + str(names))
        txt = ""
        for idx, val in enumerate(names):
            txt += "{}: {} {}".format(idx, val[0], val[1]) + "\n"

        while len(txt) > 2000:
            await message.channel.send(txt[:2000])
            txt = txt[2000:]
            print(txt)
        await message.channel.send(txt)

    #players
    if message.content == "{}players".format(prefix):
        msg = "Players: \n"
        for i in loadUsers():
            msg += "- " + i.steamName + "\n"
        while len(msg) > 2000:
            await message.channel.send(msg[:2000])
            msg = msg[2000:]
            print(msg)
        await message.channel.send(msg)

    #shreck
    if message.content == "{}shreck".format(prefix):
        msg = open("shreck.txt").read()
        while len(msg) > 2000:
            await message.channel.send(msg[:2000])
            msg = msg[2000:]
            print(msg)
        await message.channel.send(msg)

    #levels
    if message.content.startswith("{}levels".format(prefix)):
        parts = message.content.split(" ")
        users = loadUsers()
        print("levels")
        arg = message.content.split(" ")[1]
        try:
            arg = int(arg)
        except:
            await message.channel.send("argument not an integer")
        await printUsers(loadUsers(), message.channel, arg)

    #connect
    if message.content.startswith("{}connect".format(prefix)):
        parts = message.content.split(" ")
        users = loadUsers()
        discordID = message.author.id
        print("connect")
        arg = message.content.split(" ")[1]
        try:
            int(arg)
        except:
            await message.channel.send("argument not an integer")
        for i in users:
            if i.steamID == arg:
                i.discordID = discordID
                await message.channel.send("account connected to {} ".format(i.steamName))
                break
        writeUsers(users)


    #getdiscord
    if message.content.startswith("{}getdiscord".format(prefix)):
        parts = message.content.split(" ")
        steamName = parts[1]
        print(steamName)

        for i in loadUsers():
            if i.steamName == steamName:
                if i.discordID == "":
                    await message.channel.send("{} is not connected to a discord account".format(steamName))
                else:
                    await message.channel.send("{} is connected to {}".format(steamName, message.guild.get_member(i.discordID).nick))

def addOwnedGames(givenid, games):
    addUser(givenid)
    make_object = getgames.SteamGameGrabber()
    results = make_object.call_all(givenid)
    if isinstance(results, str):
        return results
    if len(results) == 0:
        return "no games found, profile is probably private"
    for result in results:
        for game in games:
            if game.gameName == result:
                if givenid not in game.steamIDs:
                    game.steamIDs.append(givenid)
                break
        else:
            games.append(gamefinderbot_gameclass.Game(results[result], result, [givenid]))
    return games

async def printGames(games, channel, amount=10):
        print(games)
        games = sorted(games)
        #games.reverse()
        msg = "**top {} most owned games**".format(amount)
        msg += "\ngame: **owners**"
        for i in range(amount ):
            msg += "\n{}: **{}**".format(games[i].gameName, games[i].getOwners())
        while len(msg) > 2000:
            await channel.send(msg[:2000])
            msg = msg[2000:]
            print(msg)
        await channel.send(msg)

async def printUsers(users, channel, amount=10):
    users = sorted(users)
    msg = "**top {} highest steam leveled players**".format(amount)
    msg += "\nplayer: **level**"
    for i in range(amount):
        msg += "\n{}: **{}**".format(users[i].steamName, users[i].steamLevel)
    while len(msg) > 2000:
        await channel.send(msg[:2000])
        msg = msg[2000:]
        print(msg)
    await channel.send(msg)

def loadGames():
    games = []
    try:
        with open("gamefinderbot_games.txt", 'r') as read_file:
            games = jsonpickle.decode(read_file.read())
    except:
        None
    return games

def getAllGameNames(games):
    names = {}
    for i in games:
        names[i.gameName] = i
    return names

def writeGames(games):
    with open("gamefinderbot_games.txt", 'w') as write_file:
        write_file.write(jsonpickle.encode(games))

def writeUsers(users):
    for i in users:
        print(i)
    with open("gamefinderbot_users.txt", 'w') as write_file:
        write_file.write(jsonpickle.encode(users))

def loadUsers():
    users = []
    try:
        with open("gamefinderbot_users.txt", 'r') as read_file:
            users = jsonpickle.decode(read_file.read())
    except:
        None
    return users

def find(key, allGameNames):
        matches = difflib.get_close_matches(key, allGameNames.keys(), n=2)
        return matches

def addUser(userID):
    users = loadUsers()
    for i in users:
        if i.steamID == userID:
            break
    else:
        users.append(gamefinderbot_userclass.User(userID))
    writeUsers(users)

print("ok" + str(loadUsers()))

client.run('NzU1ODQzOTQwNDIyNTE2ODA2.X2JMhg.LzJNpiKbHfM7WEUQxe6WzoG-Jec')