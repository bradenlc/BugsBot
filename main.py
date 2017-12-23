import discord
import asyncio
import random
import json
import logging
import SH
import config

logging.basicConfig(level=logging.INFO)

client = discord.Client()

def initRoles(message):
    roleDict = {}
    uniqueRoles = []
    membersAndUR = {}
    simCount = 0
    duplicateMembers = []
    noUniques = []
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
                    if not m in membersAndUR:
                        membersAndUR[m]=r
                    else:
                        duplicateMembers.append(m)
                        membersAndUR.pop(m)
    for m in message.server.members:
        try:
            membersAndUR[m]
        except KeyError:
            if not m in duplicateMembers:
                noUniques.append(m)
    print("Unique Roles: ")
    for x in membersAndUR:
        print(x.name + ' : ' + membersAndUR[x].name)
    print("Members with multiple unique roles: ")
    for x in duplicateMembers:
        print(x.name)
    print("Members without unique roles:")
    for x in noUniques:
        print(x.name)

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
    config.SHInstances = {}
    for x in client.get_all_channels():
        config.SHInstances[x.id] = SH.SHInstance(x, client)

async def executeUserCommands(message, command):
    #Adds user to playerlist
    if command == '!join':
        if (not config.SHInstances[message.channel.id].checkIfJoined(message)) and (not config.SHInstances[message.channel.id].gameStarted):
            config.SHInstances[message.channel.id].innedPlayerlist.append(message.author)
            await client.send_message(message.channel, 'You\'ve successfully joined the player list, <@{}>. There are currently {} players waiting for the game to start.'.format(message.author.id,str(len(config.SHInstances[message.channel.id].innedPlayerlist))))
        elif config.SHInstances[message.channel.id].gameStarted:
            await client.send_message(message.channel, "There's already a game in session")
        else:
            await client.send_message(message.channel, 'You\'re already on the player list!')

    #Removes player from playerlist
    elif command == '!leave':
        if config.SHInstances[message.channel.id].checkIfJoined(message) and not config.SHInstances[message.channel.id].gameStarted:
            config.SHInstances[message.channel.id].innedPlayerlist.remove(message.author)
            await client.send_message(message.channel, 'You\'ve successfully removed yourself from the playerlist')
        elif config.SHInstances[message.channel.id].gameStarted:
            await client.send_message(message.channel, 'You can\'t leave! The game is in session!')
        else:
            await client.send_message(message.channel, 'You\'re not on the player list!')

    #Starts game, if playerlist has 5 or more players and the author is one of them                                  
    elif command == '!start':
        if config.SHInstances[message.channel.id].checkIfJoined(message) and not config.SHInstances[message.channel.id].gameStarted:
            if len(config.SHInstances[message.channel.id].innedPlayerlist) > 4:
                config.SHInstances[message.channel.id].gameStarted = True
                await SH.startGame(message)
            else:
                await client.send_message(message.channel, 'You need at least 5 players to start a game!')
        elif config.SHInstances[message.channel.id].gameStarted:
            await client.send_message(message.channel, "A game is already in session")
        else:
            await client.send_message(message.channel, 'You need to be on the player list to start the game')

    #Currently just an interface. Will later trigger reminder
    elif command == '!remindme':
        reminder = message.content[10:]
        if reminder.startswith('to '):
            reminder = reminder[3:]
        reminder = reminder.replace("my","your")
        remind(reminder,message.author)
        await client.send_message(message.channel, 'Ok, <@' + message.author.id + '>, I\'ll remind you to ' + reminder + '.')
        
    elif command == '!addquote':
        #Add quote to server list
        pass
        
    elif command == '!quote':
        #Post quote from server
        pass

    #Identifies all members with unique roles, all members without unique roles, and all members who have multiple unique roles. Just diagnostic
    elif command == '!initroles':
        initRoles(message)

async def executeAdminCommands(message, command):
    #Temporarily blocks a user from reading or posting in the chat   
    if command == '!bedtime':
        await bedtime(message)

    #Sets a reminder for another user   
    elif command == '!remind':
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

async def executeGameCommands(message, command):
    game = config.SHInstances[message.channel.id]
    messageString = ""
    if command == "!gamestatus":
        pass
    
    elif command == "!playerlist":
        messageString = "The current living players are: "
        presidentString = "{} is President.\n".format(game.president.name)
        chancellorString = ""
        nominatedString = ""
        termLimit1 = ""
        termLimit2 = ""
        for x in game.innedPlayerlist:
            messageString = messageString + "{}, ".format(x.name)
            if x == game.nominatedPlayer:
                nominatedString = "{} is currently nominated for Chancellor.\n".format(x.name)
            if x == game.chancellor:
                chancellorString = "{} is currently Chancellor.\n".format(x.name)
            if x == game.lastChancellor:
                termLimit1 = "{} was just Chancellor, so they can't be nominated.\n".format(x.name)
            if x == game.lastPresident:
                termLimit2 = "{} was just President, so they can't be nominated.\n".format(x.name)
        messageString = messageString + presidentString + chancellorString + nominatedString + termLimit1 + termLimit2
        await client.send_message(message.channel, messageString)
                
    elif command == "!votelist":
        for x in game.voteArray:
            if game.voteArray[x] == "Uncast":
                messageString = messageString + "{} has not yet voted\n".format(x.name)
            else:
                messageString = messageString + "{} has voted {}\n".format(x.name, game.voteArray[x])
        await client.send_message(message.channel, messageString)

@client.event
async def on_message(message):
    if message.content.startswith('!'):
        tempArray = message.content.split(" ")
        command = tempArray[0].lower()
        
        if command in config.userCommands:
            await executeUserCommands(message, command)
            
        elif command in config.adminCommands:
            if (await isAdmin(message)):
                await executeAdminCommands(message, command)
                
        elif command in config.gameCommands:
            if config.SHInstances[message.channel.id].gameStarted:
                await executeGameCommands(message, command)
            else:
                await client.send_message(message.channel, "No game is running in this channel!")

        elif command in config.affirmatives or command in config.negatives:
            pass
        
        else:
            await client.send_message(message.channel, 'That\'s not a valid command')

    #Dad jokes ftw        
    elif message.content.startswith('I am '):
        print("test1")
        tempArray = message.content.split(" ")
        if len(tempArray)<4:
            await client.send_message(message.channel, "Hi {}, I'm BugsBot!".format(tempArray[2]))
    elif message.content.startswith('I\'m '):
        tempArray = message.content.split(" ")
        if len(tempArray)<3:
            await client.send_message(message.channel, "Hi {}, I'm BugsBot!".format(tempArray[1]))

            
client.run("Mzg2OTYzOTIyMDEzNjUwOTU1.DR6Aog.lL29j1S5y5nfSux0r7lVgvPry5Y")
