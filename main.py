import discord
import asyncio
import random
import logging
import config
import SH
import roles
import superfight
import deepworldAPI

logging.basicConfig(level=logging.INFO)

client = discord.Client()

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

def sendHelpMessage(message):
    if isAdmin(message):
        await client.send_message(message.channel, "`!gamemode [mode]` - Changes the mode of the game you’re playing. Current options are SH (5-10 players), Villain (3-10 players), or Duel (3 players)\n`!rules` - Gives a link to a copy of of the rules of the game you’re currently playing\n`!join` - Add yourself to the player list\n`!leave` - Remove yourself from the player list \n`!start` - Begins the game. Requires the correct number of players on the player list. Only someone on the playerlist can start the game.\n`!endgame` - Ends the game early. This requires a majority of players to use this command\n`!nameme [name]` - Sets the name of your unique role to “name”. If you don’t have a unique role, and your server has fewer than 225 roles, it gives you one. Requires the bot to have the ability to edit your role\n`!colorme [hex code]` - Sets the color of your unique role to your hex code. If you don’t have a unique role, and your server has fewer than 225 roles, it gives you one. Requires the bot to have the ability to edit your role. If you have a differently colored role that’s shared between multiple people, a server mod or admin may have to raise your unique role on the heiarchy for your color to have any effect.\nCommands are not case sensitive. If they appear to be, or if there are any other errors, please contact me directly. My discord account is Bugsy#9977")
    else:
        await client.send_message(message.author, "`!gamemode [mode]` - Changes the mode of the game you’re playing. Current options are SH (5-10 players), Villain (3-10 players), or Duel (3 players)\n`!rules` - Gives a link to a copy of of the rules of the game you’re currently playing\n`!join` - Add yourself to the player list\n`!leave` - Remove yourself from the player list \n`!start` - Begins the game. Requires the correct number of players on the player list. Only someone on the playerlist can start the game.\n`!endgame` - Ends the game early. This requires a majority of players to use this command\n`!nameme [name]` - Sets the name of your unique role to “name”. If you don’t have a unique role, and your server has fewer than 225 roles, it gives you one. Requires the bot to have the ability to edit your role\n`!colorme [hex code]` - Sets the color of your unique role to your hex code. If you don’t have a unique role, and your server has fewer than 225 roles, it gives you one. Requires the bot to have the ability to edit your role. If you have a differently colored role that’s shared between multiple people, a server mod or admin may have to raise your unique role on the heiarchy for your color to have any effect.\nCommands are not case sensitive. If they appear to be, or if there are any other errors, please contact me directly. My discord account is Bugsy#9977")
    
@client.event
async def on_ready():
    print(client.user.name, end="")
    print(client.user.id, end="")
    print("is up and running!")

async def executeUserCommands(message, command):
    
    #Currently just an interface. Will later trigger reminder
    if command == '!remindme':
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
        await roles.initRoles(message, client)

    elif command == "!colorme":
        await roles.colorMe(message, client)

    elif command == "!nameme":
        await roles.nameMe(message, client)

<<<<<<< HEAD
    elif command in ["!help", "!commands"]:
        await sendHelpMessage(message)
=======
    elif command == "!world":
        await deepworldAPI.main(message, client)

    elif command == "!stats":
        await deepworldAPI.playerProfile(message, client)
>>>>>>> 25402167236ee7c182278dd70df64b2c3a6b2747

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

    if command == '!gamemode':
        requestedGamemode = message.content[10:].split(" ")[0].lower()
        if requestedGamemode == "sh":
            config.gameInstances[message.channel.id] = SH.SHInstance(message.channel, client)
            await client.send_message(message.channel, "Your gamemode has been set to SH")
        elif requestedGamemode == "villain":
            config.gameInstances[message.channel.id] = superfight.Villain(message.channel, client)
            await client.send_message(message.channel, "Your gamemode has been set to Villain Fight")
        elif requestedGamemode == "duel":
            config.gameInstances[message.channel.id] = superfight.Duel(message.channel, client)
            await client.send_message(message.channel, "Your gamemode has been set to Duel")
        else:
            await client.send_message(message.channel, "That's not a recognized game mode")

    #If config.gameInstances[message.channel.id] throws KeyError, specify that the channel's gamemode is "Unselected"     
    try:
        game = config.gameInstances[message.channel.id]
    except KeyError:
        game = "Unselected"

    if not game == "Unselected":
        #Adds user to playerlist
        if command == '!join':
            if (not game.checkIfJoined(message)) and (not game.started):
                game.innedPlayerlist.append(message.author)
                await client.send_message(message.channel, ("You've successfully joined the player list, <@{}>. There are currently {} players waiting for the "
                                                            "game to start.".format(message.author.id,str(len(game.innedPlayerlist)))))
            elif game.started:
                await client.send_message(message.channel, "There's already a game in session")
            else:
                await client.send_message(message.channel, 'You\'re already on the player list!')

        #Removes player from playerlist
        elif command == '!leave':
            if game.checkIfJoined(message) and not game.started:
                game.innedPlayerlist.remove(message.author)
                await client.send_message(message.channel, 'You\'ve successfully removed yourself from the playerlist')
            elif game.started:
                await client.send_message(message.channel, 'You can\'t leave! The game is in session!')
            else:
                await client.send_message(message.channel, 'You\'re not on the player list!')

        #Starts game, if playerlist has 5 or more players and the author is one of them                                  
        elif command == '!start':
            print("Start message received")
            print(game.gameMode)
            if game.gameMode == "SH":
                if game.checkIfJoined(message) and not game.started:
                    if len(game.innedPlayerlist) > 4 and len(game.innedPlayerlist) < 11:
                        game.started = True
                        await SH.startGame(message)
                    else:
                        await client.send_message(message.channel, 'You need 5-10 players to start a game!')
                elif game.started:
                    await client.send_message(message.channel, "A game is already in session")
                else:
                    await client.send_message(message.channel, 'You need to be on the player list to start the game')
            elif game.gameMode == "Duel":
                print("Start message interpreted - Duel")
                if game.checkIfJoined(message) and not game.started:
                    if len(game.innedPlayerlist) == 3:
                        game.started = True
                        game.arbiterCounter = random.randrange(0, len(game.innedPlayerlist))
                        await superfight.main(game)
                    else:
                        await client.send_message(message.channel, 'You need 3 players to start a game!')
                elif game.started:
                    await client.send_message(message.channel, "A game is already in session")
                else:
                    await client.send_message(message.channel, 'You need to be on the player list to start the game')
            elif game.gameMode == "Villain":
                print("Start message interpreted")
                if game.checkIfJoined(message) and not game.started:
                    if len(game.innedPlayerlist) > 2 and len(game.innedPlayerlist) < 11:
                        game.started = True
                        game.arbiterCounter = random.randrange(0, len(game.innedPlayerlist))
                        await superfight.main(game)
                    else:
                        await client.send_message(message.channel, 'You need 3-10 players to start a game!')
                elif game.started:
                    await client.send_message(message.channel, "A game is already in session")
                else:
                    await client.send_message(message.channel, 'You need to be on the player list to start the game')

        #Begins voting to end the game
        elif command == "!endgame":
                if game.endArray == {} and not game.over:
                    await client.send_message(message.channel, ("{} has begun a vote to end the game early. This requires a majority of the current players to pass. "
                                                                "Please say `!endgame` if you'd like to be counted.").format(message.author))
                    game.endArray[message.author] = True
                elif not game.over:
                    game.endArray[message.author] = True
                    await client.send_message(message.channel, "{} has added their name to those who want to end the game. So far, there are {} "
                                              "players requesting this".format(message.author, len(game.endArray)))
                    if len(game.endArray) > game.numOfPlayers / 2:
                        game.over = True
                        await client.send_message(message.channel, "The game has been ended early!")
    else:
        await client.send_message(message.channel, "You haven't specified a game mode!")


async def executeSHCommands(message, command):
    try:
        game = config.gameInstances[message.channel.id]
        messageString = ""
        if command == "!gamestatus":
            await client.send_message(message.channel, "There are currently {} Fascist policies and {} Liberal policies enacted".format(game.facistPolicies,
                                                                                                                                        game.liberalPolicies))
                                      
        elif command == "!playerlist":
            messageString = "The current living players are: "
            presidentString = ""
            chancellorString = ""
            nominatedString = ""
            termLimit1 = ""
            termLimit2 = ""
            for x in game.innedPlayerlist:
                messageString = messageString + "{}, ".format(x.name)
                if x == game.president:
                    presidentString = "{} is President.\n".format(game.president.name)
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
                    messageString = messageString + "{} has voted `{}`\n".format(x.name, game.voteArray[x])
            await client.send_message(message.channel, messageString)
    
        elif command == "!pinchhit":
            pass

    except KeyError:
        game = False
        if command in ["!gamestatus", "!playerlist", "!votelist"]:
            client.send_message(message.channel, "That command doesn't work in this channel!")

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
            await executeGameCommands(message, command)

        elif command in config.SHCommands:
            await executeSHCommands(message, command)

        elif command in config.affirmatives or command in config.negatives:
            pass
        
        else:
            await client.send_message(message.channel, 'That\'s not a valid command')

    """#Dad jokes ftw        
    elif message.content.startswith('I am '):
        tempArray = message.content.split(" ")
        if len(tempArray)<4:
            await client.send_message(message.channel, "Hi {}, I'm BugsBot!".format(tempArray[2]))
    elif message.content.startswith('I\'m '):
        tempArray = message.content.split(" ")
        if len(tempArray)<3:
            await client.send_message(message.channel, "Hi {}, I'm BugsBot!".format(tempArray[1]))"""

client.run("Mzg2OTYzOTIyMDEzNjUwOTU1.DShlPw.gN02f-KluqdcH22sc-by7q_hLaU")
