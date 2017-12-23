import discord
import random
import asyncio
import logging
import config

class SHInstance:
    def __init__(self, gameChannel, client):
        self.client = client
        self.gameChannel = gameChannel
        self.presidentCounter = 0
        self.fascistsPolicies = 0
        self.liberalPolicies = 0
        self.numOfPlayers = 0
        self.gameMode = 0
        self.gameStarted = False
        self.voteOutcome = False
        self.nominatedPlayer = False
        self.newfascist = False
        self.president = False
        self.chancellor = False
        self.hitler = False
        self.enactedPolicy = False
        self.over = False
        self.vetoEnabled = False
        self.unanimousVeto = False
        self.lastChancellor = False
        self.lastPresident = False
        self.peekEnabled = False
        self.voteArray = {}
        self.turnDeck = []
        self.fascists = []
        self.innedPlayerlist = []
        self.policyDeck = ["fascist","fascist","fascist","fascist","fascist","fascist","fascist","fascist","fascist","fascist","fascist",
                           "Liberal","Liberal","Liberal","Liberal","Liberal","Liberal"]
        self.fullDeck = ["fascist","fascist","fascist","fascist","fascist","fascist","fascist","fascist","fascist","fascist","fascist",
                         "Liberal","Liberal","Liberal","Liberal","Liberal","Liberal"]

    def checkIfJoined(self, message):
        for innedPlayer in self.innedPlayerlist:
            if innedPlayer == message.author:
                return True
        return False

    def addfascist(self):
        self.newfascist = self.innedPlayerlist[random.randrange(1,self.numOfPlayers)]
        if self.newfascist in self.fascists:
            self.addfascist()
        else:
            self.fascists.append(self.newfascist)

    def addHitler(self):
        self.hitler = self.innedPlayerlist[random.randrange(1,self.numOfPlayers)]
        if self.hitler in self.fascists:
            self.addHitler()

    def assignRoles(self):
        self.fascists = []
        for x in range(0,self.numOffascists):
            self.addfascist()
        self.addHitler()

    async def sendMessages(self):
        if self.gameMode == 1:
            print(self.hitler.name + " is Hitler")
            print(self.fascists[0].name + " is fascist")
            await self.client.send_message(self.hitler, "You're Hitler. Your fascist teammate is " + self.fascists[0].name)
            await self.client.send_message(self.fascists[0], "You're a fascist. Your job is to help Hitler, " + self.hitler.name)
        elif self.gameMode == 2:
            await self.client.send_message(self.hitler, "You're Hitler. Because you have more than one teammate, you don't get to know who they are")
            await self.client.send_message(self.fascists[0], "You're a fascist. Your teammate is {} and Hitler is {}".format(self.fascists[1].name, self.hitler.name))
            await self.client.send_message(self.fascists[1], "You're a fascist. Your teammate is {} and Hitler is {}".format(self.fascists[0].name, self.hitler.name))
        elif self.gameMode == 3:
            await self.client.send_message(self.fascists[0], ("You're a fascist. Your teammates are {} and {}. "
                                                              " Hitler is {}.").format(self.fascists[1].name, self.fascists[2].name, self.hitler.name))
            await self.client.send_message(self.fascists[1], ("You're a fascist. Your teammates are {} and {}. "
                                                              " Hitler is {}.").format(self.fascists[0].name, self.fascists[2].name, self.hitler.name))
            await self.client.send_message(self.fascists[2], ("You're a fascist. Your teammates are {} and {}. "
                                                              " Hitler is {}.").format(self.fascists[0].name, self.fascists[1].name, self.hitler.name))
            await self.client.send_message(self.hitler, "You're Hitler. Because you have more than one teammate, you don't get to know who they are")
            
    async def assignPres(self):
        self.president = self.innedPlayerlist[self.presidentCounter%self.numOfPlayers]
        await self.client.send_message(self.gameChannel, ("The president is <@{}>.\nPresident, please nominate a player for Chancellor "
                                                          "by using `!nominate @playername`").format(self.president.id))

    async def nomination(self):
        playerNominated = False
        warningGiven = False
        while not playerNominated:
            nominationMessage = await self.client.wait_for_message(author=self.president, channel = self.gameChannel)
            try:
                self.nominatedPlayer = nominationMessage.mentions[0]
                if self.nominatedPlayer in self.innedPlayerlist:
                    if (self.nominatedPlayer != self.lastChancellor) and (self.nominatedPlayer != self.lastPresident):
                        playerNominated = True
                        await self.client.send_message(self.gameChannel, ("President {} has nominated {} for Chancellor. Please preface your vote with an '!'. Most "
                                                                          "forms of 'yes' or 'no' are supported.").format(self.president.name,
                                                                                                                          self.nominatedPlayer.name))
                    else:
                        self.nominatedPlayer = False
                        await self.client.send_message(self.gameChannel, "I'm sorry, but your nominee was term limited! Please nominate someone else.")
                else:
                    self.nominatedPlayer = False
                    await self.client.send_message(self.gameChannel, "You didn't enter a valid nomination message!")
            except IndexError:
                if not warningGiven:
                    await self.client.send_message(self.gameChannel, "Please mention the person you're nominating like this: `@user`")
                    warningGiven = True

    async def vote(self):
        self.voteArray = {}
        votesCast = 0
        for player in self.innedPlayerlist:
            self.voteArray[player] = "Uncast"
        while not votesCast==self.numOfPlayers:
            votingMessage = await self.client.wait_for_message()
            if votingMessage.content.startswith("!") and (votingMessage.author in self.innedPlayerlist) and votingMessage.content in config.affirmatives:
                if self.voteArray[votingMessage.author] == "Uncast":
                    votesCast = votesCast + 1
                    await self.client.send_message(self.gameChannel, "{} has cast a vote".format(votingMessage.author.name))
                else:
                    await self.client.send_message(self.gameChannel, "{} has changed their vote".format(votingMessage.author.name))
                self.voteArray[votingMessage.author] = "Yes"
            elif votingMessage.content.startswith("!") and (votingMessage.author in self.innedPlayerlist) and votingMessage.content in config.negatives:
                if self.voteArray[votingMessage.author] == "Uncast":
                    votesCast = votesCast + 1
                    await self.client.send_message(self.gameChannel, "{} has cast a vote".format(votingMessage.author.name))
                else:
                    await self.client.send_message(self.gameChannel, "{} has changed their vote".format(votingMessage.author.name))
                self.voteArray[votingMessage.author] = "No"

    async def countVote(self):
        yesVotes = 0
        noVotes = 0
        for player in self.innedPlayerlist:
            if self.voteArray[player] == "Yes":
                yesVotes = yesVotes + 1
            elif self.voteArray[player] == "No":
                noVotes = noVotes + 1
        messageString = ""
        for x in self.voteArray:
            messageString = messageString + "{} voted {}\n".format(x.name, self.voteArray[x])
        self.client.send_message(self.gameChannel, messageString)
        print("No votes: {}\nYes votes: {}".format(noVotes,yesVotes))
        if yesVotes > noVotes:
            return True
        else:
            return False

    async def genPolicies(self):
        self.turnDeck = []
        if len(self.policyDeck) > 3:
            i = 0
            while i < 3:
                chosenPolicy = random.randrange(0,len(self.policyDeck))
                self.turnDeck.append(self.policyDeck.pop(chosenPolicy))
                i = i + 1
        elif len(self.policyDeck) == 3:
            self.turnDeck = self.policyDeck
            self.policyDeck = self.fullDeck
        else:
            self.policyDeck = self.fullDeck
            self.genPolicies()
        print(self.turnDeck)
        if self.peekEnabled:
            self.peekEnabled = False
            await self.client.send_message(self.president, "You peeked at the following 3 policies:")
            await self.client.send_message(self.president, "1: {}".format(self.turnDeck[0]))
            await self.client.send_message(self.president, "2: {}".format(self.turnDeck[1]))
            await self.client.send_message(self.president, "3: {}".format(self.turnDeck[2]))

    async def presPolicies(self):
        await self.client.send_message(self.president, "You drew the following 3 policies:")
        await self.client.send_message(self.president, "1: {}".format(self.turnDeck[0]))
        await self.client.send_message(self.president, "2: {}".format(self.turnDeck[1]))
        await self.client.send_message(self.president, "3: {}".format(self.turnDeck[2]))
        await self.client.send_message(self.president, "Please select a policy to discard by saying '!d #'")
        def check(reply):
            bool1 = (reply.content == "!d 1" or reply.content == "!d 2" or reply.content == "!d 3")
            bool2 = reply.channel.is_private
            return (bool1 and bool2)
        reply = await self.client.wait_for_message(author=self.president, check=check)
        if reply.content == "!d 1":
            self.turnDeck.pop(0)
        elif reply.content == "!d 2":
            self.turnDeck.pop(1)
        else:
            self.turnDeck.pop(2)

    async def chancellorPolicies(self):
        await self.client.send_message(self.chancellor, "You were passed the following 2 policies:")
        await self.client.send_message(self.chancellor, "1: {}".format(self.turnDeck[0]))
        await self.client.send_message(self.chancellor, "2: {}".format(self.turnDeck[1]))
        await self.client.send_message(self.chancellor, "Please select a policy to enact by saying '!e #'")
        def check(reply):
            bool1 = (reply.content == "!e 1" or reply.content == "!e 2" or (reply.content=="!veto" and self.vetoEnabled == True))
            bool2 = reply.channel.is_private
            return (bool1 and bool2)
        reply = await self.client.wait_for_message(author=self.chancellor, check=check)
        if reply.content == "!e 1":
            self.enactedPolicy = self.turnDeck[0]
        elif reply.content == "!e 2":
            self.enactedPolicy = self.turnDeck[1]
        else:
            await self.client.send_message(self.gameChannel, "The Chancellor has chosen to veto the agenda. <@{}>, do you agree?".format(self.president.id))
            properReply = False
            while not properReply:
                reply = await self.client.wait_for_message(author=self.president)
                if reply in config.affirmatives:
                    self.unanimousVeto = True
                    properReply = True
                elif reply in config.negatives:
                    self.unanimousVeto = False
                    properReply = True
                else:
                    await self.client.send_message(self.gameChannel, "That wasn't a recognized answer. Try again, please")

    async def presInvestigate(self):
        await self.client.send_message(self.president, "Who would you like to investigate? Your choices are:")
        for x in range(len(self.innedPlayerlist)):
            nextPlayer = "{}: {}".format(x+1, self.innedPlayerlist[x])
            await self.client.send_message(self.president, nextPlayer)
        await self.client.send_message(self.president, "Please respond with a number between 1 and {}".format(x+1))


        properResponse = False
        bool1 = True
        while not (bool1 and properResponse):
            reply = await self.client.wait_for_message(author=self.president)
            if not reply.channel.is_private:
                bool1 = False
            if bool1:
                try:
                    int(reply.content)
                    for y in range(len(self.innedPlayerlist)):
                        if y == int(reply.content) - 1:
                            if not self.president == self.innedPlayerlist(y):
                                properResponse = True
                            else:
                                await self.client.send_message(self.president, "I'm pretty sure you don't want to investigate yourself. Let's try that again")
                                bool1 = False
                    if not (properResponse):
                        if bool1:
                            await self.client.send_message(self.president, "The number you entered was out of range")
                            bool1 = False
                except TypeError:
                    self.client.send_message(self.president, "That was not a valid integer! Try again")
                    bool1 = False

                    
        if (self.innedPlayerlist[int(reply) - 1]) in self.fascists or (self.innedPlayerlist[int(reply) - 1] == self.hitler):
            self.client.send_message(self.president, "{} is a member of the fascist party!".format(self.innedPlayerlist[int(reply) - 1].name))
        else:
            self.client.send_message(self.president, "{} is a member of the Liberal party.".format(self.innedPlayerlist[int(reply) - 1].name))

    async def presKill(self):
        await self.client.send_message(self.president, "Who would you like to kill? Your choices are:")
        for x in range(len(self.innedPlayerlist)):
            nextPlayer = "{}: {}".format(x+1, self.innedPlayerlist[x])
            await self.client.send_message(self.president, nextPlayer)
        await self.client.send_message(self.president, "Please respond with a number between 1 and {}".format(x+1))
        async def check(reply):
            try:
                int(reply.content)
            except TypeError:
                self.client.send_message(self.president, "That was not a valid integer! Try again")
                return False
            for y in range(len(self.innedPlayerlist)):
                if y == int(reply.content) - 1:
                    if not self.president == self.innedPlayerlist(y):
                        return True
                    else:
                        await self.client.send_message(self.president, "I'm pretty sure you don't want to kill yourself. Let's try that again")
                        await self.client.send_message(self.president, "If you are feeling suicidal, please call the suicide prevention hotline at 1-800-273-8255")
            await self.client.send_message(self.president, "The number you entered was out of the range")
            return False
        reply = await self.client.wait_for_message(author=self.president, check=check)
        killedPlayer = self.innedPlayerlist.pop(int(reply) - 1)
        self.numOfPlayers = self.numOfPlayers - 1
        self.client.send_message(self.gameChannel, "{} has been killed!".format(killedPlayer.name))
        self.over = self.checkIfWon()

    async def addPolicy(self, policy):
        if policy == "fascist":
            self.fascistsPolicies = self.fascistsPolicies + 1
            if self.fascistsPolicies == 2:
                await self.presInvestigate()
            elif self.fascistsPolicies == 3:
                self.peekEnabled = True
            elif self.fascistsPolicies == 4:
                await self.presKill()
            elif self.fascistsPolicies == 5:
                self.vetoEnabled = True
            
        elif policy == "Liberal":
            self.liberalPolicies = self.liberalPolicies + 1
            
        else:
            self.client.send_message(self.gameChannel, "The policies aren't given as a string argument!") #Should never happen, just diagnostic

    async def checkIfWon(self):
        onlyfascists = True
        for innedPlayer in self.innedPlayerlist:
            if not innedPlayer in self.fascists:
                onlyfascists = False
        if (self.fascistsPolicies == 6):
            self.client.send_message(self.gameChannel, "The fascists enacted 6 policies! They win!")
        elif(self.fascistsPolicies >= 2 and self.chancellor == self.hitler):
            self.client.send_message(self.gameChannel, "The fascists elected Hitler as Chancellor! They win!")
        elif onlyfascists:
            self.client.send_message(self.gameChannel, "The only living players are fascists! They win!")
        elif (self.liberalPolicies == 5):
            self.client.send_message(self.gameChannel, "The Liberals have enacted 6 policies! They win!")
        elif not (self.hitler in self.innedPlayerlist):
            self.client.send_message(self.gameChannel, "The Liberals have killed Hitler! They win!")
        else:
            return False
        return True

    async def trollAonar(self):
        for x in self.innedPlayerlist:
            if x.id == "263436294020005888" or x.id == 263436294020005888:
                await self.client.send_message(x, "Use the following link to see your role: <https://goo.gl/9iFFHz>")

async def startGame(message):
    game = config.SHInstances[message.channel.id]
    #await game.trollAonar()
    game.numOfPlayers = len(game.innedPlayerlist)
    if game.numOfPlayers > 8:
        game.numOffascists = 3
        game.gameMode = 3
    elif game.numOfPlayers > 6:
        game.numOffascists = 2
        game.gameMode = 2
    else:
        game.numOffascists = 1
        game.gameMode = 1
    game.assignRoles()
    await game.sendMessages()
    game.presidentCounter = random.randrange(0,game.numOfPlayers)
    await mainGame(game)

async def mainGame(game):
    while not game.over:
        print("Test 832")
        await game.genPolicies()
        failedElections = 0
        playerElected = False
        while not playerElected:
            await game.assignPres()
            await game.nomination()
            await game.vote()
            game.voteOutcome = await game.countVote()
            if game.voteOutcome:
                game.chancellor = game.nominatedPlayer
                game.nominatedPlayer = False
                game.over = await game.checkIfWon()
                if game.over:
                    break
                else:
                    await game.client.send_message(game.gameChannel, ("The vote succeeded! President {} and Chancellor {} "
                                                                      "are now choosing policies.").format(game.president.name, game.chancellor.name))
                game.lastChancellor = False
                game.lastPresident = False
                await game.presPolicies()
                await game.chancellorPolicies()
                if not game.unanimousVeto:
                    playerElected = True
                else:
                    await game.genPolicies()
                    failedElections = failedElections + 1
            elif failedElections<2:
                failedElections = failedElections + 1
                game.presidentCounter = game.presidentCounter + 1
            else:
                topPolicy = game.turnDeck.pop(0)
                game.policyDeck.append(turnDeck[0])
                game.policyDeck.append(turnDeck[1])
                await game.addPolicy(topPolicy)
                await game.client.send_message(game.gameChannel, "Because 3 governments failed, a {} policy was enacted at random".format(topPolicy))
                failedElections = 0
                await game.genPolicies()
                game.presidentCounter = game.presidentCounter+1
                game.over = await game.checkIfWon()
        if game.over:
            break
        else:
            await game.addPolicy(game.enactedPolicy)
            await game.client.send_message(game.gameChannel, "President {} and Chancellor {} have enacted a {} policy".format(game.president.name,
                                                                                                                              game.chancellor.name,
                                                                                                                              game.enactedPolicy))
            game.lastChancellor = game.chancellor
            game.lastPresident = game.president
            game.chancellor = False
            game.over = await game.checkIfWon()
            game.presidentCounter += 1
    config.SHInstances[game.gameChannel.id] = SHInstance(game.gameChannel, game.client)
    
