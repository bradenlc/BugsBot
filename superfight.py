import discord
import random
from gameSuperclass import *

class Superfight(GameInstance):
    def __init__(self, gameChannel, client, gameMode):
        super().__init__(gameChannel, client, gameMode)
        self.fullAttrDeck = ["10 Of Them", "10 Of Them", "10 Stories Tall", "10 Stories Tall", "10 Stories Tall", "100 Of Them", "100 Of Them", "100 Stories Tall",
                             "100 Stories Tall", "3 Of Them", "3 Of Them", "3 Stories Tall", "3 Stories Tall", "3 Stories Tall", "3-Foot Fingernails",
                             "50 Of Them", "50 Of Them", "6 Inches Tall", "6 Inches Tall", "9 Feet Tall", "9 Feet Tall", "Acid Blood", "Afraid Of Water",
                             "Agoraphobic", "Allergic To All Animals", "Armed With A Bacon-Wrapped Baseball Bat", "Armed With A Barbed Wore Net",
                             "Armed With A Cannon", "Armed With A Catapult And Unlimited Livestock", "Armed With A Cattle Prod", "Armed With A Chainsaw",
                             "Armed With A Crowbar", "Armed With A Flamethrower", "Armed With A Freeze Ray", "Armed With A Harpoon Gun", "Armed With A Lightsaber",
                             "Armed With A Live T-Rex On A Stick", "Armed With A Long Electrified Whip", "Armed With A Machine Gun", "Armed With A Nail Gun",
                             "Armed With A Poison-Tipped Lance", "Armed With A Portal Gun", "Armed With A Puppy Musket", "Armed With A Rocket Launcher",
                             "Armed With A Sadness Ray", "Armed With A Samurai Sword", "Armed With A Shotgun", "Armed With A Shotgun That Shoots Shotguns",
                             "Armed With A Shrink Ray", "Armed With A Sniper Rifle", "Armed With A Superglue Fire Hose", "Armed With A Tranquilizer Gun",
                             "Armed With A Trident", "Armed With An  Infinite Sausage Lasso", "Armed With An Impenetrable Shield", "Armed With Axe",
                             "Armed With Catarangs", "Armed With Cupid'S Bow", "Armed With Dynamite", "Armed With Ghost Pepper Spray",
                             "Armed With Holy Hand Grenades", "Armed With Nunchucks", "Armer With A Bow And Unlimited Arrows", "Balancing On A Circus Ball",
                             "Being Guarded By The Secret Service", "Believes They Are Invisible", "Bionic", "Breathes Fire", "Can Animate Dirt",
                             "Can Become Any Animal", "Can Become Mist While Holding Breath", "Can Blow 200-Mph Winds", "Can Breathe Underwater",
                             "Can Clone Self But Each Clone Is Half As Smart As The Previous", "Can Clone Self But Each Clone Is Half The Size Of The Previous",
                             "Can Control Gravity", "Can Control Hair", "Can Control Machines", "Can Control Opponent'S Right Hand", "Can Control Plants",
                             "Can Create A Hologram Of Self", "Can Dig And Run Through Tunnels With Super Speed", "Can Fly",
                             "Can Fly But Only Two Feet Above The Ground", "Can Fly If Nobody Is Watching", "Can Hold Breathe Forever", "Can Kill With A Kiss",
                             "Can Make A Force Field While Holding Breath", "Can Match Opponent'S Size", "Can Only Be Killed By Beheading",
                             "Can Only Move By Back Flipping", "Can Only Move When Opponent Moves", "Can Only See Movement",
                             "Can Possess Opponent For 30 Seconds Then Gets Very Tired", "Can Read Minds", "Can Run 200 Mph But Only In A Straight Line",
                             "Can See 3 Seconds Into The Future", "Can Stop Time While Holding Breath", "Can Stretch Like Rubber",
                             "Can Summon Am Army Internet Trolls", "Can Summon Anything From A Hardware Store", "Can Take The Form Of Anything They Touch",
                             "Can Take The Form Of Anything Water-Based", "Can Teleport But Goes Blind For 10 Seconds After Each Use", "Can Throw Sticky Bombs",
                             "Can Turn Into Any Vehicle", "Can Turn Invisible While Singing Snow Tunes", "Can Turn To Steel", "Can Walk Through Sold Objects",
                             "Can'T See", "Can'T Stop Clapping", "Can'T Stop Dancing", "Can'T Stop Laughing", "Can'T Stop Sobbing", "Can'T Turn Left",
                             "Carrying A Baby", "Carrying Way Too Many Grocery Bags", "Catlike Reflexes", "Clothes Are Way Too Big", "Clothes Are Way Too Tight",
                             "Constantly Taking Selfies", "Controls A Tween Army", "Controls All Animals", "Controls An Army Of Flying Monkeys", "Controls Magnetism",
                             "Controls Weather", "Covered In Eyes", "Covered In Spikes", "Distracted By Shiny Things", "Driving A Tank", "Driving Popemobile",
                             "Entire Body Is Very Sticky", "Everything The Touch Turns To Hummus", "Explodes If The Stop Moving",
                             "Figuratively \"On Fire\" ...And Literally", "Floating Down On A Parachute", "Frost Breath ", "Handcuffed To Golf Cart",
                             "Hands Are Covered In Butter", "Hands Glued To Hips", "Has A 6-Foot Neck", "Has A Battleship", "Has A Beard Made Bees", "Has A Hostage",
                             "Has A Magical Unicorn Horn", "Has A Skunk On A Stick", "Has A Time Machine Phone Booth", "Has A Voodoo Doll Of Opponent",
                             "Has An Invisible Cloak", "Has An Invisible Jet", "Has Feet Instead Of Hands", "Has Hands Instead Of Feet",
                             "Has Jellyfish Instead Of Hands", "Has Majestic Flamming Antlers Growing Of Head", "Has No Bones", "Has One Tiny Baby Arm",
                             "Has Telekinesis", "Has Tiny Bird Legs", "Has Tiny T-Rex Arms", "Has Two Extra Arms", "Has Two Peg Legs", "Has Vertigo",
                             "Has X-Ray Vision", "Heals 100 Times Faster Than Normal", "Horrible Self-Esteem", "In a Berserker Rage", "In A Blimp",
                             "In A Helicopter", "In A Hot Air Balloon", "In A Jet Fighter", "In A Space Suit", "Inside A Giant Hamster Ball", "Invisible",
                             "Is A 1000 Years Old", "Is A Baby", "Is A Belieber And Is Convinced Opponent Means Bieber Bodily Harm", "Is A Hoarder", "Is A Hypnotist",
                             "Is A Piñata", "Is A Stuffed", "Is A Super Genius", "Is A Tween", "Is Amish", "Is Drunk", "Is Elderly", "Is Having A Really Good Hair Day",
                             "Is Made Of Guacamole", "Is Rabid", "Is Radioactive", "Is Really Hangry", "Is Really Into Fonts", "Is Really Really Good-Looking",
                             "Is Really Really Stupid", "Just Drank Five Energy Drinks", "Killed By Water", "Knows Knug Fu", "Laser Eyes", "Lays Exploding Eggs",
                             "Leeches Opponent'S Health When Touched", "Literal Jazz Hands", "Literally Wearing Beer Goggles", "Literally Wearing Heart On Sleeve",
                             "Locked In A Antique Diver'S Helmet", "Locked In A Shark Cage", "Long Metal Claws Pop Out Of Hands", "Made Of Lava", "Made Of Mirrors",
                             "Made Of Paper", "Made Of Sand", "Made Of Stone", "Megafighter!", "Morbidly Obese", "Mustache Can Stretch And Move At Will", "Narcoleptic",
                             "No Arms", "No Depth Perception", "No Legs", "On A Jet Ski", "On A Pogo Stick", "On A Segway", "On A Velocipede", "On Stilts",
                             "Only Has One Leg", "Pacifist", "Piloting An Attack Drone", "Pregnant", "Really Clumsy", "Really Really Has To Pee",
                             "Relies On Heat Vision To See", "Relies On Sonar To See", "Riding A Battle Cat", "Riding A Broomstick", "Riding A Depressed Centaur",
                             "Riding A Flying Narwhal", "Riding A Horse", "Riding A Hoverboard", "Riding A Motorcycle", "Riding A War Elephant", "Scissor Hands",
                             "Screams Names Of Attacks Before Using Them", "Shoots Acid", "Shoots Bees From Mouth", "Shoots Blinding Light From Hands", "Shoots Glitter",
                             "Shoots Laughing Gas", "Shoots Lightning", "Shoots Poison Darts From Nose", "Shoots Tear Gas", "Shoots Webs",
                             "Slows Time When Eyes Are Closed", "Sonic Scream", "Sprays Neurotoxin", "Stone Gaze", "Suffering From Delusions Of Grandeur",
                             "Summons Cats To Do Bidding", "Super Endurance", "Super Jump", "Super Strength", "Swinging A Shark On A Chain",
                             "Thinks The Floor Is Actually Lava", "Throwing Spears", "Throws 200-Mph Fastballs", "Throws Antiques", "Throws Bears", "Throws Burritos",
                             "Throws Fireballs", "Throws Knives", "Throws Ninja Stars", "Tongue Can Stretch And Move At Will", "Trapped In A Potato Sack",
                             "Two Extra Legs", "Unaffected By Impact", "Used To Be A Bear", "Uses The Force", "Venomous Bite", "Walking Twelve Wiener Dogs",
                             "Wall-Crawler", "Wearing A Flaming Tutu", "Wearing A Impenetrable Tuxedo", "Wearing A Jetpack", "Wearing A Meat Bikini",
                             "Wearing A Robotic Exoskeleton", "Wearing A Scuba Suit", "Wearing A Suit Of Armor", "Wearing A Tin Foil Hat", "Wearing Cement Shoes",
                             "Wearing One Of Those Cones They Put On Pets To Keep Them From Licking Themselves", "Wearing Rocket-Powered Roller Skates",
                             "Wearing Sharpened Stilettos", "Wearing Skis", "With A Prehensile Tail", "Armed With A Dubstep Gun", "Armed With A Gatling Gun",
                             "Armed With A Lightsaber That Has Two Smaller Lightsabers Sticking Out Of The Hilt", "Armed With A Machete",
                             "Armed With A Piranha Launcher", "Armed With A Railgun", "Armed With A Really Really Bright Laser Pointer",
                             "Armed With A Surface-To-Air Missile Launcher", "Armed With A Limitless Loot Crate", "Can Call Orbital Bombardments",
                             "Can Fly...At The Speed Of Molasses", "Can Leap Over Tall Buildings In A Single Bound", "Can Only Be Killer By A Shot To The Head",
                             "Can Only Be Killer By A Stake Through The Heart", "Can Summon Infinite Trampolines", "Cannons Instead Of Hands",
                             "Chained To Their Evil Twin", "Commands An Army Of Disposable Minions", "Covered In Gasoline", "Everything They Touch Turns Inside Out",
                             "Flaming Hands", "Has An Enormous Exposed Brain", "In A Flying Saucer", "Is Faster Than A Speeding Bullet", "Is Really Really Emotional",
                             "Is Really Really Good At Parkour ...Really", "Leading A Team Of Trained Velociraptors", "Literally A Gift", "Machine Guns For Legs",
                             "Regrows Body Parts At Will", "Riding A Nuclear Missile", "Shoots Lasers Out Of Ears", "Stuck In One Of Those Electric Cars For Toddlers",
                             "Swinging A Two-Ton Tuna", "Throws Water Billions Filled With Acid", "Wearing A Bubble Wrap Suit", "Wearing A Scuba Suit",
                             "Wrapped In Toilet Paper"]
        self.fullCharDeck = ["101 Dalmatians", "Abraham Lincoln", "Alien", "Angel", "Apache Warrior", "Assassin", "Barney", "Billionaire Playboy", 
                             "Blob", "Bodybuilder", "Boy Band", "Boy Scout", "Bruce Lee", "Bull", "Cactus", "Canada", "Carnie", "Cat", "Cheetah",
                             "Child Beauty Pageant Queen", "Chimpanzee", "Chuck Norris", "Coachella Lineup", "College A Cappella Group", "Conan", "Conjoined Twins",
                             "Cowboy", "Crazy Cat Lady", "Crocodile Hunter", "Darth Vader", "Demon", "Demon-Possessed Car", "Dexter", "Disembodied Head", "Dolphin",
                             "Dragon", "E.T.", "Eagle", "Electric Eel", "Emperor Penguin", "Everyone At Burning Man", "Evil Doll", "Fainting Goat", "Femme Fatale",
                             "Forrest Gump", "Frankenstein", "Freddy", "French Bulldog", "Gandhi", "Genghis Khan", "George W. Bush", "Giant Squid", "Giraffe",
                             "Girl Scout", "Gladiator", "Google", "Gorilla", "Grim Reaper", "Hannibal", "Heisenberg", "Helen Keller", "Hermione",
                             "High School Marching Band", "Hillary Clinton", "Hippo", "Hipster", "Hobo", "Hockey Player", "Homer", "Hulk", "Hunchback",
                             "Identical Twins", "Iron Man", "Jack Bauer", "Jason", "Justin Bieber", "K-Pop Star", "Katniss", "Kindergarten Class", "Leprechaun",
                             "Literally Insane Clown Posse", "Lucha Libre Wrestler", "Macgyver", "Mad Scientist", "Mafia Don", "Mario Brothers.", "Marshmallow Man",
                             "Martha Stewart", "Me", "Meatloaf", "Men In Black", "Mermaid", "Michael Jackson", "Mike Tyson", "Miley Cyrus", "Mime", "Moose",
                             "Mr. Rogers", "Mummy", "Musketeer", "My Boss", "My Ex", "My Significant Other", "Nigerian Prince", "Ninja", "Nudist", "Obama",
                             "Octopus", "Olympic Gymnast", "Owl", "Pet Rock", "Pick A Celebrity", "Pick A Comic Book Character", "Pick A Movie Character",
                             "Pick A TV Character", "Pick An Action Movie Star", "Pirate", "Polar Bear", "Psychic", "Pterodactyl", "Pikachu", "Queen", "Rambo",
                             "Redneck", "Reggae Band", "Rhinoceros", "Robin Hood", "Robot", "Saber-Toothed Tiger", "Samurai", "Sasquatch", "Secret Agent",
                             "Senior Citizen Bowling Team", "Shark", "Sharpshooter", "Sherlock Holmes", "Skeleton", "Sloth", "Smoke Monster", "Snake", "Soccer Mom",
                             "Spartan", "Spider", "Stephen Hawking", "Street Fighter", "Sumo Wrestler", "Supermodel", "Swarm Of Killer Bees", "T-Rex", "Terminator",
                             "The Devil", "The Doctor", "The Dude", "The Illuminati", "The Kardashians", "The Player To Your Left", "The Pope", "The Statue Of Library",
                             "The U.N.", "Turtle", "Ultimate Fighting Champion", "Unicorn", "Vampire", "Vampire Slayer", "Vegan", "Velociraptor", "Viking", "Werewolf",
                             "Whale", "Willy Wonka", "Witch", "Wizard", "Wooly Mammoth", "Your Mom", "Amazon Warrior", "Animorph", "Army Of Skeletons", "Ash",
                             "Carnivorous Plant", "Derby Girl", "Dr. Horrible", "France", "Godzilla", "Goliath", "Grizzly Bear", "Hercules", "Honey Badger", "Hydra",
                             "Iron Giant", "Kaiju", "Keanu Reeves", "King Kong", "King Rather", "Literal Teen Wolf", "Loch Ness Monster", "Mothra", "Ocelot",
                             "Poltergeist", "Prince Charming", "Raccoon", "Sandy Cheeks", "Star Lord", "Stegosaurus", "Sushi Chef", "Swarm Of Piranhas",
                             "The Common Cold", "The Navy", "The Player To Your Right", "Trapper", "Two Tribbles", "Water Buffalo", "Yeti", "Zombie"]
        self.attrDeck = self.fullAttrDeck
        self.charDeck = self.fullCharDeck
        self.dealTo = []
        self.victor = False
        self.arbiter = False
        self.character = {}
        self.playerDeck = {}
        self.attributes = {}
        self.scoreboard = {}
        self.charSelectionStatus = {}
        self.attrSelectionStatus = {}
        self.arbiterCounter = 0

    async def dealCards(self):
        cardsToDeal = len(self.dealTo)*3
        if len(self.attrDeck) < cardsToDeal:
            self.attrDeck = self.fullAttrDeck
        if len(self.charDeck) < cardsToDeal:
            self.charDeck = self.fullCharDeck
        self.playerDeck = {}
        for player in self.dealTo:
            self.playerDeck[player] = [[],[]]
            for x in range(0,3):
                self.playerDeck[player][0].append(self.charDeck.pop(random.randrange(0,len(self.charDeck))))
                self.playerDeck[player][1].append(self.attrDeck.pop(random.randrange(0,len(self.attrDeck))))
            await self.client.send_message(player, ("You received the following characters:\n1) {}\n2) {}\n3) {}\nYou also received the following attributes:\n"
                                               "1) {}\n2) {}\n3) {}").format(self.playerDeck[player][0][0], self.playerDeck[player][0][1], self.playerDeck[player][0][2],
                                                                             self.playerDeck[player][1][0], self.playerDeck[player][1][1], self.playerDeck[player][1][2]))

    async def receiveFighters(self):
        self.charSelectionStatus = {}
        self.attrSelectionStatus = {}
        allSelected = False
        for player in self.dealTo:
            self.charSelectionStatus[player] = "Unselected"
            self.attrSelectionStatus[player] = "Unselected"
            self.attributes[player] = []
            await self.client.send_message(player, ("Please choose a character with `!c` followed by the number of the character you'd like to select, and an attribute "
                                               "with `!a` followed by the number for the attribute you'd like to select"))
        while not allSelected:
            reply = await self.client.wait_for_message()
            if self.over:
                break
            if reply.author in self.dealTo and reply.channel.is_private:
                if reply.content.startswith("!"):
                    splicedReply = reply.content.lower().split("!")
                else:
                    splicedReply = reply.content.lower().split("!")[1:]
                for x in range(0, len(splicedReply)):
                    if splicedReply[x].startswith("c"):
                        splicedReply[x] = splicedReply[x][1:]
                        while splicedReply[x].startswith(" "):
                            splicedReply[x] = splicedReply[x][1:]
                        try:
                            if splicedReply[x][0] in ["1", "2", "3"]:
                                self.charSelectionStatus[reply.author] = self.playerDeck[reply.author][0][int(splicedReply[x][0]) - 1]
                                await self.client.send_message(reply.author, "Your character selection was received")
                        except IndexError:
                            await self.client.send_message(reply.author, "Please use this format: `!c #`")
                    if splicedReply[x].startswith("a"):
                        splicedReply[x] = splicedReply[x][1:]
                        while splicedReply[x].startswith(" "):
                            splicedReply[x] = splicedReply[x][1:]
                        try:
                            if splicedReply[x][0] in ["1", "2", "3"]:
                                self.attrSelectionStatus[reply.author] = int(splicedReply[x][0]) - 1
                                await self.client.send_message(reply.author, "Your attribute selection was received")
                        except IndexError:
                            await self.client.send_message(reply.author, "Please use this format: `!a #`")
                allSelected = self.checkAllSelected()
        for player in self.dealTo:
            self.character[player] = self.charSelectionStatus[player]
            self.attributes[player].append(self.playerDeck[player][1].pop(self.attrSelectionStatus[player]))
                
    def checkAllSelected(self):
        for player in self.dealTo:
            if self.charSelectionStatus[player] == "Unselected" or self.attrSelectionStatus[player] == "Unselected":
                print("Failed on {}".format(player.name))
                return False
        print("Succeeded")
        return True
    
    async def revealFighters(self):
        characterAnnouncementString = ""
        for player in self.dealTo:
            playerString = "{}'s fighter is `{}`, with the following modifiers:\n".format(player.name, self.character[player])
            i = 1
            for attribute in self.attributes[player]:
                playerString = playerString + "{}) {}\n".format(i, attribute)
                i += 1
            characterAnnouncementString = characterAnnouncementString + playerString + "\n"
        await self.client.send_message(self.gameChannel, characterAnnouncementString)

    async def assignArbiter(self):
        self.arbiter = self.innedPlayerlist[self.arbiterCounter%len(self.innedPlayerlist)]
        if self.gameMode == "Duel":
            await self.client.send_message(self.arbiter, "You're the arbiter for this round")
        elif self.gameMode == "Villain":
            await self.client.send_message(self.arbiter, "You're the villain this round")
        else:

    def createDealList(self):
        self.dealTo = []
        for player in self.innedPlayerlist:
            if not player == self.arbiter:
                self.dealTo.append(player)

    async def findWinner(self, nameToCall):
        if nameToCall == "Villain":
            messageString = ""
            i = 1
            for player in self.dealTo:
                messageString = messageString + "\n{}) {}".format(i, player.name)
                i += 1
            await self.client.send_message(self.gameChannel, ("Villain, please choose who you think would best defeat your character. You can choose by typing "
                                                         "`!select @user`. Your options are: " + messageString + "\nPlayers, you may argue your case. The Villain "
                                                         "may choose at whatever time they like, so convince them quickly!"))
        elif nameToCall == "Arbiter":
            messageString = ""
            i = 1
            for player in self.dealTo:
                messageString = messageString + "\n{}) {}".format(i, player.name)
            await self.client.send_message(self.gameChannel, ("Arbiter, please choose which character you think would win in a fight. You can choose by typing "
                                                         "`!select @user`. Your options are: " + messageString + "\nPlayers, you may argue your case. The Arbiter "
                                                         "may choose at whatever time they like, so convince them quickly!"))
        def checkSelection(reply):
            if reply.content.startswith("!select"):
                try:
                    self.victor = reply.mentions[0]
                    if self.victor in self.dealTo:
                        return True
                    else:
                        return False
                except IndexError:
                    return False
        reply = await self.client.wait_for_message(author = self.arbiter, check = checkSelection)
        self.scoreboard[reply.mentions[0]] += 1

    async def giveRandomAttr(self):
        if len(self.attrDeck) < len(self.dealTo):
            self.attrDeck = self.fullAttrDeck
        for player in self.dealTo:
            self.attributes[player].append(self.attrDeck[random.randrange(0,len(self.attrDeck))])
                    

class Villain(Superfight):
    def __init__(self, gameChannel, client):
        super().__init__(gameChannel, client, "Villain")

    async def playRemainingAttr(self):
        i = 0
        while not i == 2*len(self.dealTo):
            if i < len(self.dealTo):
                await self.client.send_message(self.gameChannel, "{} is now playing an attribute".format(self.dealTo[i].name))
                await self.client.send_message(self.dealTo[i], ("You have the remaining cards:\n1) {}\n2) {}\nPlease respond with the number of the card you'd like to "
                                                                "play and the user that you'd like to play it on. Note: You are permitted to play it on yourself, if you "
                                                                "so choose. Please note that because you need to mention the player, this must be done in the channel "
                                                                "in which the game is currently taking place.").format(self.playerDeck[self.dealTo[i]][1][0],
                                                                                                                       self.playerDeck[self.dealTo[i]][1][1]))
                sufficientReply = False
                warningGiven = False
                while not sufficientReply:
                    reply = await self.client.wait_for_message(author = self.dealTo[i])
                    if reply.channel == self.gameChannel:
                        number = False
                        user = False
                        parsedReply = reply.content.split(" ")
                        for word in parsedReply:
                            if word in ["1", "2"]:
                                number = int(word)
                        if not number == False:
                            number -= 1
                            try:
                                user = reply.mentions[0]
                                if user in self.innedPlayerlist:
                                    playedCard = self.playerDeck[reply.author][1].pop(number)
                                    self.attributes[user].append(playedCard)
                                    await self.client.send_message(self.gameChannel, "{} has played the modifier `{}` on {}".format(self.dealTo[i].name, playedCard,
                                                                                                                               user.name))                                                                                                                           
                                    sufficientReply = True
                                else:
                                    await self.client.send_message(self.gameChannel, "Please only play cards on people who are in the game!")
                            except:
                                await self.client.send_message(self.gameChannel, "Please only tag the player you'd like to play a card on")
                        elif (not sufficientReply) and (not warningGiven):
                            await self.client.send_message(self.gameChannel, "Please use the following formats: `# @user` or `@user #`")
                            warningGiven = True
            else:
                x = i-len(self.dealTo)
                await self.client.send_message(self.gameChannel, "{} is now playing an attribute".format(self.dealTo[x].name))
                await self.client.send_message(self.dealTo[x], ("Your last remaining card is {}. Please tag the user you'd like to "
                                                                "play it on.").format(self.playerDeck[self.dealTo[x]][1][0]))
                sufficientReply = False
                while not sufficientReply:
                    reply = await self.client.wait_for_message(author = self.dealTo[x])
                    if reply.channel == self.gameChannel:
                        try:
                            user = reply.mentions[0]
                            if user in self.innedPlayerlist:
                                playedCard = self.playerDeck[self.dealTo[x]][1].pop(0)
                                self.attributes[user].append(playedCard)
                                await self.client.send_message(self.gameChannel, "{} has played the modifier `{}` on {}".format(self.dealTo[x].name, playedCard,
                                                                                                                           user.name))
                                sufficientReply = True
                            else:
                                await self.client.send_message(self.gameChannel, "Please only play cards on people who are in the game!")
                        except:
                            pass
            i += 1

class Duel(Superfight):
    def __init__(self, gameChannel, client):
        super().__init__(gameChannel, client, "Duel")

def initScoreboard(game):
    for player in game.innedPlayerlist:
        game.scoreboard[player] = 0

async def printScoreboard(game):
    scoreboardString = "Scoreboard:"
    for player in game.innedPlayerlist:
        scoreboardString = scoreboardString + "\n{}: `{}`".format(player.name, game.scoreboard[player])
    await game.client.send_message(game.gameChannel, scoreboardString)

async def main(game):
    myIterator = 0
    initScoreboard(game)
    while myIterator != len(game.innedPlayerlist) and not game.over:
        await game.assignArbiter()
        if game.gameMode == "Villain":
            await game.client.send_message(game.gameChannel, "The Villain is choosing cards")
            game.dealTo = [game.arbiter]
            await game.dealCards()
            await game.receiveFighters()
            await game.giveRandomAttr()
            await game.revealFighters()
        game.createDealList()
        await game.dealCards()
        await game.client.send_message(game.gameChannel, "Players are now choosing their fighters")
        await game.receiveFighters()
        if game.gameMode == "Villain":
            await game.revealFighters()
            await game.client.send_message(game.gameChannel, "Players will now take turns playing their remaining attributes on eachother or themselves one by one")
            await game.playRemainingAttr()
            await game.revealFighters()
            game.dealTo = [game.arbiter]
            await game.revealFighters()
            await game.findWinner("Villain")
        else:
            await game.giveRandomAttr()
            await game.revealFighters()
            await game.findWinner("Arbiter")
        await printScoreboard(game)
        game.arbiterCounter += 1
        myIterator += 1
    await game.client.send_message(game.gameChannel, "Everyone has had a turn to be judge, so the game has ended.")
    config.gameInstances[game.gameChannel.id] = Villain(game.gameChannel, game.client)



    
