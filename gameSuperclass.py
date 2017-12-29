class GameInstance:
    def __init__(self, gameChannel, client, gameMode):
        self.client = client
        self.gameChannel = gameChannel
        self.innedPlayerlist = []
        self.over = False
        self.started = False
        self.endArray = {}
        self.numOfPlayers = 0
        self.gameMode = gameMode
        print("Game object created")

    def __str__(self):
        return self.gameMode

    #Chech if player who sent message is in innedPlayerlist
    def checkIfJoined(self, message):
        for innedPlayer in self.innedPlayerlist:
            if innedPlayer == message.author:
                return True
        return False
