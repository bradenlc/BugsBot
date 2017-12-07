import discord
import random
import asyncio
import logging

async def trollAonar(game):
    for x in game.innedPlayerlist:
        if x.id == 263436294020005888:
            await send_message(x, "Use the following link to see your role: https://goo.gl/9iFFHz")

def checkIfJoined(message):
    try:
        message.channel.innedPlayerlist[0]
    except NameError:
        message.channel.innedPlayerlist = []
    for innedPlayer in message.channel.innedPlayerlist:
        if innedPlayer == message.author:
            return True
    return False

def addFacist(game):
    game.newFacist = game.innedPlayerlist[random.randrange(1,game.numOfPlayers)]
    if game.newFacist in game.facists:
        addFacist(game)
    else:
        game.facists.append(newFacist)

def addHitler(game):
    game.hitler = game.innedPlayerlist[random.randrange(1,game.numOfPlayers)]
    if game.hitler in game.facists:
        addHitler(game)

def assignRoles(game):
    game.facists = []
    for x in range(0,numOfFacists):
        addFacist(game)
    addHitler(game)

async def sendMessages(game):
    if game.gameMode == 1:
        await send_message(game.hitler, "You're Hitler. Your facist teammate is " + game.facists[0].name)
        await send_message(game.facist[0], "You're a facist. Your job is to help Hitler, " + game.hitler.name)
    elif game.gameMode == 2:
        await send_message(game.hitler, "You're Hitler. Because you have more than one teammate, you don't get to know who they are")
        await send_message(game.facist[0], "You're a facist. Your teammate is " + game.facist[1].name + " and Hitler is " + game.hitler.name)
        await send_message(game.facist[1], "You're a facist. Your teammate is " + game.facist[0].name + " and Hitler is " + game.hitler.name)
    elif game.gameMode == 3:
        await send_message(game.facist[0], "You're a facist. Your teammates are " + game.facist[1].name + " and " + game.facist[2].name + ". Hitler is " + game.hitler.name)
        await send_message(game.facist[1], "You're a facist. Your teammates are " + game.facist[2].name + " and " + game.facist[2].name + ". Hitler is " + game.hitler.name)
        await send_message(game.facist[2], "You're a facist. Your teammates are " + game.facist[1].name + " and " + game.facist[0].name + ". Hitler is " + game.hitler.name)
        await send_message(game.hitler, "You're Hitler. Your teammates are " + game.facist[0].name + ", " + game.facist[1].name + " and " + game.facist[2].name)
        
async def assignPres(game):
    game.president = game.innedPlayerList[game.presidentCounter%game.numOfPlayers]
    await send_message(game, "The president is " + game.president.name)

async def startGame(message):
    game = message.channel
    await trollAonar(game)
    game.numOfPlayers = len(message.channel.innedPlayerlist)
    if game.numOfPlayers > 8:
        game.numOfFacists = 3
        game.gameMode = 3
    elif game.numOfPlayers > 6:
        game.numOfFacists = 2
        game.gameMode = 2
    else:
        game.numOfFacists = 1
        game.gameMode = 1
    assignRoles(game)
    await sendMessages(game)
    game.presidentCounter = random.randrange(0,game.numOfPlayers)
    while not game.over:
        await assignPres(game)
        #Turn of game here
        game.presidentCounter += 1
    
