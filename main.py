import discord
import asyncio
import random
import json
import logging

logging.basicConfig(level=logging.INFO)

client = discord.Client()

def initRoles(message):
    roleDict = {}
    uniqueRoles = []
    membersAndUR = {}
    simCount = 0
    duplicateMembers = []
    for r in message.server.roles:
        roleDict[r] = 0
    for m in message.server.members:
        for mr in m.roles:
            roleDict[mr] += 1
    for r in roleDict:
        if roleDict[r] == 1:
            uniqueRoles.append(r)
    for r in uniqueRoles:
        for m in message.server.members:
            for mr in m.roles:
                if mr == r:
                    membersAndUR[m]=r
    for m1 in membersAndUR:
        for m2 in membersAndUR:
            if m1 == m2:
                simCount += 1
            if simCount == 2:
                duplicateMembers.append(m1)
        simCount = 0
    for m in duplicateMembers:
        for m2 in membersAndUR:
            if m1 == m2:
                membersAndUR.pop(m1)
    print("Unique Roles: ")
    for x in membersAndUR:
        print(x + ' : ' + membersAndUR[x])
    print("Duplicate Members: ")
    for x in duplicateMembers:
        print(x)
                    
        

def checkIfJoined(player):
    for innedPlayer in innedPlayerlist:
        if innedPlayer == player:
            return True
    return False

async def isAdmin(message):
    if message.author.server_permissions.manage_server and message.author.server_permissions.manage_roles:
        return True 
    await client.send_message(message.channel, 'You don\'t have permission to use that command')
    return False

def remind(reminder, whoToRemind):
    #Add people to list of people to remind
    #Message the list periodically with reminders
    pass
    
def bedtime(message):
    if isAdmin(message.author):
        #Set 'bedtime' for user based on message parsing
        pass
    
@client.event
async def on_ready():
    print(client.user.name, end="")
    print(client.user.id, end="")
    print("is up and running!")
    print('------')
    global innedPlayerlist
    innedPlayerlist = []

@client.event
async def on_message(message):
    if message.content.startswith('!'):
        if message.content.startswith('!join'):
            if (not checkIfJoined(message.author)):
                innedPlayerlist.append(message.author)
                await client.send_message(message.channel, 'You\'ve successfully joined the player list, <@{}>. There are currently {} players waiting for the game to start.'.format(message.author.id,str(len(innedPlayerlist))))
            else:
                await client.send_message(message.channel, 'You\'re already on the player list!')
                
        elif message.content.startswith('!start'):
            if playerList.length() > 4:
                #Start game based on inned playerlist
                pass
            else:
                await client.send_message(message.channel, 'You need at least 5 players to start a game!')
            
        elif message.content.startswith('!remindMe'):
            reminder = message.content[10:]
            if reminder.startswith('to '):
                reminder = reminder[3:]
            reminder = reminder.replace("my","your")
            remind(reminder,message.author)
            await client.send_message(message.channel, 'Ok, <@' + message.author.id + '>, I\'ll remind you to ' + reminder + '.')
            
        elif message.content.startswith('!addquote'):
            if not quoteList:
                with open("Bugsbot/quoteList.pk1","r") as quoteFile:
                    quoteList = json.load(quoteFile)
            quoteList[len(quoteList)] = message.content[9:]
            with open("Bugsbot/quoteList.pk1","w") as quoteFile:
                json.dump(quoteList, quoteFile)
            
        elif message.content.startswith('!quote'):
            if not quoteList:
                with open("Bugsbot/quoteList.pk1","r") as quoteFile:
                    quoteList = json.load(quoteFile)
            await client.send_message(message.channel, quoteList[random.randrange(0,len(quoteList))])
            
        elif message.content.startswith('!bedtime'):
            if isAdmin(message):
                await bedtime(message)
              
        elif message.content.startswith('!remind '):
            if (await isAdmin(message)):
                messageComponents = message.content.split(" ",2)
                whoToRemind = messageComponents[1]
                reminder = messageComponents[2]
                if reminder.startswith("to "):
                    reminder = reminder[3:]
                    await client.send_message(message.channel, 'Ok, <@' + message.author.id + '>, I\'ll remind ' + whoToRemind + ' to ' + reminder)
                    reminder = reminder.replace("his","your")
                    reminder = reminder.replace("her","your")
                    reminder = reminder.replace("their","your")
                else:
                    await client.send_message(message.channel, 'Ok, <@' + message.author.id + '>, I\'ll remind ' + whoToRemind + ' to ' + reminder)
                remind(reminder,whoToRemind)

        elif message.content.startswith('!initRoles'):
            initRoles(message)

        else:
            await client.send_message(message.channel, 'That\'s not a valid command')

client.run('Mzg2OTYzOTIyMDEzNjUwOTU1.DQYrJw.U713vS30TRd4OQ8goAEKrDdyKLo')
