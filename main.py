import discord
import asyncio
import random
import logging
import config
import SH
import roles
import superfight
import onRun
import wobSearcher

logging.basicConfig(level=logging.INFO)

client = discord.Client()

async def isAdmin(message):
    if message.author.server_permissions.manage_server and message.author.server_permissions.manage_roles:
        return True 
    await client.send_message(message.channel, 'You don\'t have permission to use that command')
    return False

async def newGame(client, channel, requestedGamemode):
    if requestedGamemode == "sh":
        config.gameInstances[channel.id] = SH.SHInstance(channel, client)
        await client.send_message(channel, "Your gamemode has been set to SH")
    elif requestedGamemode == "villain":
        config.gameInstances[channel.id] = superfight.Villain(channel, client)
        await client.send_message(channel, "Your gamemode has been set to Villain Fight")
    elif requestedGamemode == "duel":
        config.gameInstances[channel.id] = superfight.Duel(channel, client)
        await client.send_message(channel, "Your gamemode has been set to Duel")
    else:
        await client.send_message(channel, "That's not a recognized game mode")

def remind(reminder, whoToRemind):
    #Add people to list of people to remind
    #Message the list periodically with reminders
    pass
    
async def bedtime(message):
    if (await isAdmin(message.author)):
        #Set 'bedtime' for user based on message parsing
        pass

async def sendHelpMessage(message):
    if (await isAdmin(message)):
        await client.send_message(message.channel, ("`!gamemode [mode]` - Changes the mode of the game you’re playing. Current options are SH (5-10 players), Villain (3-10 players), or "
                                                    "Duel (3 players)\n`!rules` - Gives a link to a copy of of the rules of the game you’re currently playing\n`!join` - Add yourself to "
                                                    "the player list\n`!leave` - Remove yourself from the player list \n`!start` - Begins the game. Requires the correct number of players"
                                                    " on the player list. Only someone on the playerlist can start the game.\n`!endgame` - Ends the game early. This requires a majority "
                                                    "of players to use this command\n`!nameme [name]` - Sets the name of your unique role to “name”. If you don’t have a unique role, and "
                                                    "your server has fewer than 225 roles, it gives you one. Requires the bot to have the ability to edit your role\n`!colorme [hex code]`"
                                                    " - Sets the color of your unique role to your hex code. If you don’t have a unique role, and your server has fewer than 225 roles, it "
                                                    "gives you one. Requires the bot to have the ability to edit your role. If you have a differently colored role that’s shared between "
                                                    "multiple people, a server mod or admin may have to raise your unique role on the heiarchy for your color to have any effect.\nCommands"
                                                    " are not case sensitive. If they appear to be, or if there are any other errors, please contact me directly. My discord account is "
                                                    "Bugsy#9977"))
    else:
        await client.send_message(message.author, ("`!gamemode [mode]` - Changes the mode of the game you’re playing. Current options are SH (5-10 players), Villain (3-10 players), or "
                                                    "Duel (3 players)\n`!rules` - Gives a link to a copy of of the rules of the game you’re currently playing\n`!join` - Add yourself to "
                                                    "the player list\n`!leave` - Remove yourself from the player list \n`!start` - Begins the game. Requires the correct number of players"
                                                    " on the player list. Only someone on the playerlist can start the game.\n`!endgame` - Ends the game early. This requires a majority "
                                                    "of players to use this command\n`!nameme [name]` - Sets the name of your unique role to “name”. If you don’t have a unique role, and "
                                                    "your server has fewer than 225 roles, it gives you one. Requires the bot to have the ability to edit your role\n`!colorme [hex code]`"
                                                    " - Sets the color of your unique role to your hex code. If you don’t have a unique role, and your server has fewer than 225 roles, it "
                                                    "gives you one. Requires the bot to have the ability to edit your role. If you have a differently colored role that’s shared between "
                                                    "multiple people, a server mod or admin may have to raise your unique role on the heiarchy for your color to have any effect.\nCommands"
                                                    " are not case sensitive. If they appear to be, or if there are any other errors, please contact me directly. My discord account is "
                                                    "Bugsy#9977"))
    
@client.event
async def on_ready():
    print(client.user.name, end=" ")
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

    elif command == "!wob":
        await client.send_message(message.channel,wobSearcher.resolveSearch(message.content))

    elif command in ["!help", "!commands"]:
        await sendHelpMessage(message)

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
        await newGame(client, message.channel, requestedGamemode)
            
    try:
        game = config.gameInstances[message.channel.id]
    except KeyError:
        game = "Unselected"

    if not game == "Unselected":

        #Resets game signups
        if command == "!restart" or command == "!reset":
            if not game.started:
                await newGame(client, message.channel, game.gameMode)
            else:
                await client.sendMessage(message.channel, "You can't restart an in-progress game!")
            
        #Adds user to playerlist
        elif command == '!join':
            if (not game.checkIfJoined(message)) and (not game.started):
                game.innedPlayerlist.append(message.author)
                await client.send_message(message.channel, ('You\'ve successfully joined the player list, <@{}>. There are currently {} players waiting for the '
                                                            'game to start.').format(message.author.id,str(len(game.innedPlayerlist))))
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
            if game.gameMode == "sh":
                if game.checkIfJoined(message) and not game.started:
                    if len(game.innedPlayerlist) > 4 and len(game.innedPlayerlist) < 11:
                        game.started = True
                        await SH.startGame(message)
                        await newGame(client, message.channel, "sh")
                    else:
                        await client.send_message(message.channel, 'You need 5-10 players to start a game!')
                elif game.started:
                    await client.send_message(message.channel, "A game is already in session")
                else:
                    await client.send_message(message.channel, 'You need to be on the player list to start the game')
            elif game.gameMode == "duel":
                if game.checkIfJoined(message) and not game.started:
                    if len(game.innedPlayerlist) == 3:
                        game.started = True
                        game.arbiterCounter = random.randrange(0, len(game.innedPlayerlist))
                        await superfight.main(game)
                        await newGame(client, message.channel, "duel")
                    else:
                        await client.send_message(message.channel, 'You need 3 players to start a game!')
                elif game.started:
                    await client.send_message(message.channel, "A game is already in session")
                else:
                    await client.send_message(message.channel, 'You need to be on the player list to start the game')
            elif game.gameMode == "villain":
                if game.checkIfJoined(message) and not game.started:
                    if len(game.innedPlayerlist) > 2 and len(game.innedPlayerlist) < 11:
                        game.started = True
                        game.arbiterCounter = random.randrange(0, len(game.innedPlayerlist))
                        await superfight.main(game)
                        await newGame(client, message.channel, "villain")
                    else:
                        await client.send_message(message.channel, 'You need 3-10 players to start a game!')
                elif game.started:
                    await client.send_message(message.channel, "A game is already in session")
                else:
                    await client.send_message(message.channel, 'You need to be on the player list to start the game')

        elif command == "!rules":
            rulesDict = {
                "sh": ("http://secrethitler.com/assets/Secret_Hitler_Rules.pdf"),
                "duel": ("This game is divided into 3 rounds, each of which have identical rules. To begin the first round, a random player is chosen as 'Arbiter'. The Arbiter serves as "
                         "the judge for the round. Each of the other two players are then dealt 3 character cards and 3 attribute cards. They then choose one of each to construct their "
                         "fighter. A second random attribute card is then added to each, and the fighters are both revealed. The Arbiter then has the ability to decide who would win "
                         "the fight. The players may try to convince the Arbiter to choose in their favor, if they want. Once the arbiter has made a choice, the role shifts and a new "
                         "round begins. Once everyone has been Arbiter, the game ends."),
                "villain": ("This game is divided into a number of rounds, each of which have identical rules. To begin the first round, a random player is chosen as 'Villain'. The "
                            "Villain is dealt 3 character cards and 3 attribute cards. They then choose one of each to construct their fighter. A second random attribute card is then "
                            "added, and their fighter is revealed. Afterwards, each other player is dealt 3 of each card type, and designs their fighter to best defeat the Villain. "
                            "Once each player is done, the fighters are all revealed, and players may play their remaining attribute cards on whichever player they like, including "
                            "themselves. Once all remaining cards are played, the Villain chooses which fighter would best beat them. That character wins.")
                }
            await client.send_message(message.author, rulesDict[game.gameMode])

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
                    if len(game.endArray) > len(game.innedPlayerlist)/2:
                        game.over = True
                        await client.send_message(message.channel, "The game has been ended early!")
    elif command in ["!join", "!leave", "!start", "!rules"]:
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
            try:
                print("{} command invoked in {}".format(command, message.server.name))
            except AttributeError:
                print("{} command invoked in a private server".format(command))
            await executeUserCommands(message, command)
            
        elif command in config.adminCommands:
            if (await isAdmin(message)):
                try:
                    print("{} command invoked in {}".format(command, message.server.name))
                except AttributeError:
                    print("{} command invoked in a private server".format(command))
                await executeAdminCommands(message, command)
                
        elif command in config.gameCommands:
            try:
                print("{} command invoked in {}".format(command, message.server.name))
            except AttributeError:
                print("{} command invoked in a private server".format(command))
            await executeGameCommands(message, command)

        elif command in config.SHCommands:
            try:
                print("{} command invoked in {}".format(command, message.server.name))
            except AttributeError:
                print("{} command invoked in a private server".format(command))
            await executeSHCommands(message, command)

        elif command in config.affirmatives or command in config.negatives:
            pass
        
        else:
            pass
            """await client.send_message(message.channel, 'That\'s not a valid command')
#Dad jokes ftw        
    elif message.content.startswith('I am '):
        tempArray = message.content.split(" ")
        if len(tempArray)<4:
            await client.send_message(message.channel, "Hi {}, I'm BugsBot!".format(tempArray[2]))
    elif message.content.startswith('I\'m '):
        tempArray = message.content.split(" ")
        if len(tempArray)<3:
            await client.send_message(message.channel, "Hi {}, I'm BugsBot!".format(tempArray[1]))"""

onRun.beginRunning(client)

