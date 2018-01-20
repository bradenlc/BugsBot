import discord
import asyncio
import logging

async def initRoles(message, client):
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
    print("/nMembers with multiple unique roles: ")
    for x in duplicateMembers:
        print(x.name)
    print("/nMembers without unique roles:")
    for x in noUniques:
        print(x.name)

async def uniqueRole(message, client):
    userRoles = []
    for role in message.author.roles:
        userRoles.append(role)
    for member in message.server.members:
        if member != message.author:
            for memberRole in member.roles:
                if memberRole in userRoles:
                    userRoles.remove(memberRole)
    try:
        uniqueRole = userRoles[0]
        return uniqueRole
    except IndexError:
        numOfRoles = 0
        for x in message.server.roles:
            numOfRoles += 1
        if numOfRoles <= 225:
            requestedName = "{}'s role".format(message.author.name)
            uniqueRole = await client.create_role(message.server, name = requestedName)
            await client.add_roles(message.author, uniqueRole)
            return uniqueRole
        else:
            await client.send_message(message.server, "You don't have a unique role, and there are too many roles to give you a new one")
            return False

async def colorMe(message, client):
    if not message.server is None:
        parseArray = message.content.split("#")
        try:
            hexCode = parseArray[1][:6]
            colorInt = discord.Color(int(hexCode, 16))
            member = message.author
            memberRole = await uniqueRole(message, client)
            if not memberRole == False:
                await client.edit_role(message.server, memberRole, color = colorInt)
                await client.send_message(message.channel, "Your color has been modified to hex code `#{}`".format(hexCode))
        except IndexError:
            await client.send_message(message.channel, "That wasn't a valid hex code. Please use the following format: `#ffffff`")
        except ValueError:
            await client.send_message(message.channel, "You didn't specify a valid hex code")
        except discord.Forbidden:
            await client.send_message(message.channel, "The bot doesn't have permission to edit your role")  
    else:
        await client.send_message(message.channel, "You can't run this command here")

async def nameMe(message, client):
    if not message.server is None:
        requestedName = message.content[7:]
        while requestedName.startswith(" "):
            requestedName = requestedName[1:]
        while requestedName.endswith(" "):
            requestedName = requestedName[:len(requestedName)-1]
        member = message.author
        memberRole = await uniqueRole(message, client)
        if not memberRole == False:
            try:
                await client.edit_role(message.server, memberRole, name = requestedName)
                await client.send_message(message.channel, "Your role name has been set to `{}`".format(requestedName))
            except discord.Forbidden:
                await client.send_message(message.channel, "The bot doesn't have permission to edit your role")
            except discord.HTTPException:
                await client.send_message(message.channel, "The bot failed to edit your role")
    else:
        await client.send_message(message.channel, "You can't run this command here")
        





    
