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

def startGame(message):

    
