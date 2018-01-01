import discord
import asyncio
import urllib.request
import webbrowser
import json

def interpret(raw):
    if raw.startswith("!world"):
        raw = raw[6:]
    while raw.startswith(" "):
        raw = raw[1:]
    while raw.endswith(" "):
        raw = raw[:len(raw)-1]
    return raw

def breakpoints(raw):
    keywordList = ["!dev", "!market", "!sort", "!pvp", "!biome"]
    breakpointList = [0]
    for keyword in keywordList:
        breakpointList.append(len(raw.split(keyword)[0]))
    breakpointList.append(len(raw))
    return breakpointList

def parseString(raw, breakpointList):
    print(breakpointList)
    parsedString = []
    for i in range(0, len(breakpointList)-1):
        parsedString.append(raw[breakpointList[i]:breakpointList[i+1]])
    print(parsedString)
    searchList = []
    for element in parsedString:
        while element.startswith(" "):
            element = element[1:]
        while element.endswith(" "):
            element = element[:len(element)-1]
        element = element.replace("=", " ")
        if not element == "":
            searchList.append(element.lower())
    return searchList

async def getURL(client, channel, searchList):
    print(searchList)
    development, activity, pvp, biome, sort, name = False, False, False, False, False, False
    for x in searchList:
        print(x)
        if not x.startswith("!"):
            name = x.replace(" ", "+")
            
        elif x.lower().startswith("!pvp"):
            pvp = True
            
        elif x.startswith("!dev ") or x.startswith("!development "):
            devArray = x.split(" ")
            try:
                if int(devArray[1]) < 6 and int(devArray[1]) >= 0:
                    development = int(devArray[1])
                else:
                    await client.send_message(channel, "You didn't enter a number between 0 and 5 for development")
            except ValueError:
                await client.send_message(channel, "You didn't enter a number for development. Development is measured from 0 to 5")
            except IndexError:
                await client.send_message(channel, "You need to have something after `{}`!".format(x))
        elif x.startswith("!dev"):
            await client.send_message(message.channel, "You need spaces between your command and your arguments")
            
        elif x.startswith("!biome "):
            requestedBiome = ((x[7:]).split(" "))[0]
            if requestedBiome in ["brain", "deep", "desert", "hell", "plain"]:
                biome = requestedBiome
            elif requestedBiome == "plains":
                biome = "plain"
            else:
                await client.send_message(channel, "The bot couldn't understand what biome you're looking for!")

        elif x.startswith("!sort "):
            requestedSort = ((x[6:]).split(" "))[0]
            print(requestedSort)
            if requestedSort in ["popularity", "popular", "pop", "busy"]:
                sort = "popularity"
            elif requestedSort in ["created", "time", "date", "new"]:
                sort = "created"

        elif x.startswith("!market"):
            print("market recognized")
            activity = "market"
            
    searchList = {"development":development,
                  "activity":activity,
                  "pvp":pvp,
                  "biome":biome,
                  "sort":sort,
                  "name":name}
    print(searchList)
    keyWord = False
    searchString = "https://api.deepworldgame.com/v1/worlds"
    for x in searchList:
        if not searchList[x] == False:
            if not keyWord:
                keyWord = True
                searchString = searchString + "?"
            else:
                searchString = searchString + "&"
            searchString = searchString + "{}={}".format(x, searchList[x])
    return searchString

def getData(url):
    data = urllib.request.urlopen(url)
    data = data.read().decode('UTF-8')
    data = json.loads(data)
    return data

def getTopTen(data):
    moreThanTen = False
    topTenList = []
    counter = 0
    for world in data:
        if counter<10:
            topTenList.append(world)
            counter += 1
        else:
            moreThanTen = True
            break
    return [topTenList, moreThanTen]

async def sendTopTen(client, channel, topTenList, moreThanTen):
    i = 1
    if moreThanTen:
        messageString = "There were many results. The top ten are below:\n"
    else:
        messageString = "There were the following {} results:\n".format(len(topTenList))
    for world in topTenList:
        worldString = "{}) {} - {} biome\n".format(i, world["name"], world["biome"])
        messageString = messageString + worldString
        i += 1
    messageString = messageString + "You can get more information on a world by typing `!info` followed by the world number. "
    if moreThanTen:
        messageString = messageString + "If you don't see your world on the list, try being more specific, to make sure it's in the top ten results."
    else:
        messageString = messageString + "If you don't see your world on the list, double check that all of the information you answered is correct."
    await client.send_message(channel, messageString)

async def getResponse(client, channel, topTenList):
    infoRequest = False
    newTopTen = False
    while not (infoRequest or newTopTen):
        reply = await client.wait_for_message(channel = channel)
        messageContent = reply.content.lower()
        if messageContent.startswith("!info"):
            messageContent = messageContent[5:]
            while messageContent.startswith(" "):
                messageContent = messageContent[1:]
            messageContent = messageContent.split(" ")
            try:
                requestedWorld = int(messageContent[0])
                if requestedWorld <= len(topTenList) and requestedWorld > 0:
                    infoRequest = True
                    return topTenList[requestedWorld-1]
                else:
                    await client.send_message(channel, "You entered a number that wasn't in range")
            except ValueError:
                await client.send_message(channel, "Please select the world using the number used to label it")
        elif messageContent.startswith("!world"):
            newTopTen = True

def getWorldInfo(world):
    try:
        worldScale = world["scale"]
    except TypeError:
        worldScale = None
    
    if worldScale is None:
        sizeString = ""
    else:
        sizeString = "{} ".format(worldScale)
        
    try:
        worldActivity = world["activity"]
        if worldActivity == "market":
            marketString = "Market world\n"
        else:
            marketString = ""
    except TypeError:
        marketString = ""
    except KeyError:
        marketString = ""

    try:
        pvpStatus = world["pvp"]
        if pvpStatus == True:
            pvpString = "Enabled"
        else:
            pvpString = "Disabled"
    except KeyError:
        pvpString = "Disabled"
    worldInfo = ("{}\n{}{} biome\n{} players currently active\n{}PVP: {}\nDevelopment: {}\nAcidity: {}\nExplored: {}%\nItems Placed: {}\nItems Mined: {}\nLife: {}"
                 "\nPlaques: {}\nLandmarks: {}\nTeleporters: {}\nProtectors: {}").format(world["name"], sizeString, world["biome"], world["players"], marketString,
                                                                                         pvpString, world["development"], world["acidity"], world["explored"]*100,
                                                                                         world["items_placed"], world["items_mined"], world["life"],
                                                                                         world["content"]["plaques"], world["content"]["landmarks"],
                                                                                         world["content"]["teleporters"], world["content"]["protectors"])
    return worldInfo

async def main(message, client):
    raw = interpret(message.content)
    breakpointList = breakpoints(raw)
    breakpointList.sort()
    searchList = parseString(raw, breakpointList)
    url = await getURL(client, message.channel, searchList)
    print(url)
    data = getData(url)
    results = getTopTen(data)
    if len(results[0]) > 1:
        await sendTopTen(client, message.channel, results[0], results[1])
        chosenWorld = await getResponse(client, message.channel, results[0])
        worldInfo = getWorldInfo(chosenWorld)
        await client.send_message(message.channel, worldInfo)
    elif len(results[0]) == 1:
        worldInfo = getWorldInfo(results[0][0])
        await client.send_message(message.channel, worldInfo)
    else:
        await client.send_message(message.channel, "There were no results for your search")
    
async def playerProfile(message, client):
    raw = message.content[6:]
    while raw.startswith(" "):
        raw = raw[1:]
    await client.send_message(message.channel, "http://www.deepworldgame.com/players/{}".format(raw.split(" ")[0]))

    
