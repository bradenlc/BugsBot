import discord
import asyncio

client = discord.Client()

def checkIfJoined(player):
    for innedPlayer in innedPlayerlist:
        if innedPlayer == player:
            return True
    return False

def remind(reminder, whoToRemind):
    #Add people to list of people to remind
    #Message the list periodically with reminders
    
def bedtime(message):
    if isAdmin(message.author):
        #Set 'bedtime' for user based on message parsing
    
@client.event
async def on_ready():
    print(client.user.name, end="")
    print(client.user.id, end="")
    print("is up and running!")
    print('------')
    innedPlayerlist = []

@client.event
async def on_message(message):
    if message.content.startswith('!'):
        if message.content.startswith('!join'):
            if not checkIfJoined(message.author):
                innedPlayerList.append(message.author)
                await client.send_message(message.channel, 'You\'ve successfully joined the player list, ' + message.author + '. There are currently ' + str(playerList.length()) + 'players waiting for the game to start.')
            else:
                await client.send_message(message.channel, 'You\'re already on the player list!')
                
        elif message.content.startswith('!start'):
            if playerList.length() > 4:
                #Start game based on inned playerlist
            else:
                await client.send_message(message.channel, 'You need at least 5 players to start a game!')
            
        elif message.content.startswith('!remindMe'):
            #Parse out '!remindMe' (Everything after first space)
            await remind(reminder,message.author)
            await client.send_message(message.channel, 'Ok, ' + message.author + ', I\'ll remind you.')
            
        elif message.content.startswith('!bedtime'):
            if isAdmin(message.author):
              await bedtime(message)
              
              
        elif message.content.startswith('!remind '):
            if isAdmin(message.author):
                #Take first UserID as whoToRemind
                #Parse out first UserID and '!remind ' (everything after second space)
                await remind(reminder,whoToRemind)
                await client.send_message(message.channel, 'Ok, ' + message.author + ', I\'ll remind ' + whoToRemind + ' to ' + reminder)
        
