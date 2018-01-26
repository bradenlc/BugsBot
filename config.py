gameInstances = {}

affirmatives = ["!y",
                "!yes",
                "!ja",
                "!yay",
                "!mhm"]

negatives = ["!n",
             "!no",
             "!nein",
             "!nay"]

gameCommands = ["!gamemode",
                "!join",
                "!leave",
                "!start",
                "!endgame",
                "!restart", "!reset",
                "!c", "!c1", "!c2", "!c3",
                "!a", "!a1", "!a2", "!a3",
                "!select",
                "!rules"]

SHCommands = ["!nominate",
              "!veto",
              "!skip",
              "!pinchhit",
              "!playerlist",
              "!votelist",
              "!gamestatus"]

userCommands = ["!remindme",
                "!addquote",
                "!quote",
                "!initroles",
                "!colorme",
                "!nameme",
                "!help",
                "!commands",
                "!world",
                "!info",
                "!stats",
                "!wob"]

adminCommands = ["!bedtime",
                 "!remind"]

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
