import discord
import random
import asyncio
import logging

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

async def assignRoles(game):
    game.facists = []
    for x in range(0,numOfFacists):
        addFacist(game)
    addHitler(game)

async def startGame(message):
    game = message.channel
    game.numOfPlayers = len(message.channel.innedPlayerlist)
    if game.numOfPlayers > 8:
        game.numOfFacists = 3
        game.gameMode = 2
    elif game.numOfPlayers > 6:
        game.numOfFacists = 2
        game.gameMode = 2
    else:
        game.numOfFacists = 1
        game.gameMode = 1
    
