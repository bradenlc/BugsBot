import discord
import random
import asyncio
import logging

async def trollAonar(game):
    for x in game.innedPlayerlist:
        if x.id == 263436294020005888:
            await client.send_message(x, "Use the following link to see your role: <https://goo.gl/9iFFHz>")

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
        await client.send_message(game.hitler, "You're Hitler. Your facist teammate is " + game.facists[0].name)
        await client.send_message(game.facist[0], "You're a facist. Your job is to help Hitler, " + game.hitler.name)
    elif game.gameMode == 2:
        await client.send_message(game.hitler, "You're Hitler. Because you have more than one teammate, you don't get to know who they are")
        await client.send_message(game.facist[0], "You're a facist. Your teammate is " + game.facist[1].name + " and Hitler is " + game.hitler.name)
        await client.send_message(game.facist[1], "You're a facist. Your teammate is " + game.facist[0].name + " and Hitler is " + game.hitler.name)
    elif game.gameMode == 3:
        await client.send_message(game.facist[0], "You're a facist. Your teammates are " + game.facist[1].name + " and " + game.facist[2].name + ". Hitler is " + game.hitler.name)
        await client.send_message(game.facist[1], "You're a facist. Your teammates are " + game.facist[2].name + " and " + game.facist[2].name + ". Hitler is " + game.hitler.name)
        await client.send_message(game.facist[2], "You're a facist. Your teammates are " + game.facist[1].name + " and " + game.facist[0].name + ". Hitler is " + game.hitler.name)
        await client.send_message(game.hitler, "You're Hitler. Your teammates are " + game.facist[0].name + ", " + game.facist[1].name + " and " + game.facist[2].name)
        
async def assignPres(game):
    game.president = game.innedPlayerlist[game.presidentCounter%game.numOfPlayers]
    await client.send_message(game, "The president is " + game.president.name)
    await client.send_message(game, "Nominate a player for Chancelor by using !nominate @playername")

async def nomination(game):
    playerNominated = False
    while not playerNominated:
        nominationMessage = await client.wait_for_message(author=game.president, channel = game)
        if nominationMessage.content.startswith("!nominate "):
            tempList = nominationMessage.content.split("<")
            if tempList[1].startswith("@"):
                game.nominatedPlayer = get_user_info(tempList[1][1:])
                playerNominated = True
                await client.send_message(game, "President {} has nominated {} for Chancellor. Please vote with '!y' or '!n'".format(game.president.name, game.nominatedPlayer.name))
            else:
                await client.send_message(game, "You didn't enter a valid nomination message!")

async def vote(game):
    game.voteArray = {}
    votesCast = 0
    for player in game.innedPlayerlist:
        game.voteArray[player] = "uncast"
    while not votesCast==game.numOfPlayers:
        votingMessage = await client.wait_for_message(channel=game)
        if votingMessage.content == "!y" and (votingMessage.author in game.innedPlayerList):
            if game.voteArray[votingMessage.author] == "uncast":
                votesCast = votesCast + 1
            game.voteArray[votingMessage.author] = True
        elif votingMessage.content == "!n" and (votingMessage.author in game.innedPlayerList):
            if game.voteArray[votingMessage.author] == "uncast":
                votesCast = votesCast + 1
            game.voteArray[votingMessage.author] = False

async def countVote(game):
    yesVotes = 0
    noVotes = 0
    for player in innedPlayerlist:
        if game.voteArray[player] == True:
            yesVotes = yesVotes + 1
        elif game.voteArray[player] == False:
            noVotes = noVotes + 1
        else:
            await client.send_message(game, "Someone voted something other than yes or no!")
            #Should never happen. Just diagnostic
    if yesVotes > noVotes:
        return True
    else:
        return False

def genPolicies(game):
    game.turnDeck = []
    if len(game.policyDeck) > 3:
        i = 0
        while i < 3:
            chosenPolicy = random.randrange(0,len(game.policyDeck))
            game.turnDeck[i] = game.policyDeck.pop(chosenPolicy)
            i = i + 1
    elif len(game.policyDeck) == 3:
        game.turnDeck = game.policyDeck
        game.policyDeck = game.fullDeck
    else:
        game.policyDeck = game.fullDeck
        genPolicies(game)

async def presPolicies(game):
    await client.send_message(game.president, "You drew the following 3 policies:")
    await client.send_message(game.president, "1: {}".format(game.turnDeck[0]))
    await client.send_message(game.president, "2: {}".format(game.turnDeck[1]))
    await client.send_message(game.president, "3: {}".format(game.turnDeck[2]))
    await client.send_message(game.president, "Please select a policy to discard by saying '!d #'")
    def check(reply):
        bool1 = (reply.content == "!d 1" or reply.content == "!d 2" or reply.content == "!d 3")
        bool2 = reply.channel.is_private
        return (bool1 and bool2)
    reply = await client.wait_for_message(author=game.president, check=check)
    if reply.content == "!d 1":
        game.turnDeck.pop(0)
    elif reply.content == "!d 2":
        game.turnDeck.pop(1)
    else:
        game.turnDeck.pop(2)

async def chancellorPolicies(game):
    await client.send_message(game.chancellor, "You were passed the following 2 policies:")
    await client.send_message(game.chancellor, "1: {}".format(game.turnDeck[0]))
    await client.send_message(game.chancellor, "2: {}".format(game.turnDeck[1]))
    await client.send_message(game.chancellor, "Please select a policy to enact by saying '!e #'")
    def check(reply):
        bool1 = (reply.content == "!e 1" or reply.content == "!e 2")
        bool2 = reply.channel.is_private
        return (bool1 and bool2)
    reply = await client.wait_for_message(author=game.chancellor, check=check)
    if reply.content == "!e 1":
        game.enactedPolicy = game.turnDeck[0]
    else:
        game.enactedPolicy = game.turnDeck[1]

async def addPolicy(game, policy):
    if policy == "Facist":
        game.facistPolicies = game.facistPolicies + 1
    elif policy == "Liberal":
        game.liberalPolicies = game.liberalPolicies + 1
    else:
        client.send_message(game, "The policies aren't given as a string argument!") #Should never happen, just diagnostic

async def checkIfWon(game):
    pass

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
    game.over = False
    game.liberalPolicies = 0
    game.facistPolicies = 0
    game.policyDeck = ["Facist","Facist","Facist","Facist","Facist","Facist","Facist","Facist","Facist","Facist","Facist","Liberal","Liberal","Liberal","Liberal","Liberal","Liberal"]
    game.fullDeck = ["Facist","Facist","Facist","Facist","Facist","Facist","Facist","Facist","Facist","Facist","Facist","Liberal","Liberal","Liberal","Liberal","Liberal","Liberal"]
    main(game)

async def main(game):
    while not game.over:
        failedElections = 0
        playerElected = False
        while not playerElected:
            await assignPres(game)
            await nomination(game)
            await vote(game)
            game.voteOutcome = countVote(game)
            if game.voteOutcome:
                game.chancellor = game.nominatedPlayer
                #game.over = await checkIfWon(game)
                if game.over:
                    break
                else:
                    await client.send_message(game, "The vote succeeded! President {} and Chancellor {} are now choosing policies.".format(game.president.name, game.chancellor.name))
                playerElected = True
            elif failedElections<2:
                failedElections = failedElections + 1
            else:
                topPolicy = game.policyDeck[random.randrange(0,len(game.policyDeck))]
                await addPolicy(game, topPolicy)
                await client.send_message(game, "Because 3 governments failed, a {} policy was enacted at random".format(topPolicy))
                failedElections = 0
                game.over = await checkIfWon(game)
        if game.over:
            break
        else:
            genPolicies(game)
            await presPolicies(game)
            await chancellorPolicies(game)
            await addPolicy(game, game.enactedPolicy)
            await send_message(game, "President {} and Chancellor {} have enacted a {} policy".format(game.president.name, game.chancellor.name, game.enactedPolicy))
            #game.over = await checkIfWon(game)
            game.presidentCounter += 1
    
