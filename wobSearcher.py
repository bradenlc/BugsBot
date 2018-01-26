import datetime

def breakpoints(inputString):
    tempList = inputString.split("!tags")
    tagsStart = len(tempList[0])
    tempList = inputString.split("!not")
    antitagsStart = len(tempList[0])
    tempList = inputString.split("!before")
    beforeStart = len(tempList[0])
    tempList = inputString.split("!after")
    afterStart = len(tempList[0])
    tempList = inputString.split("!speaker")
    speakerStart = len(tempList[0])
    tempList = inputString.split("!order")
    orderStart = len(tempList[0])
    return [tagsStart, antitagsStart, beforeStart, afterStart, speakerStart, orderStart, len(inputString)]

def parseString(inputString, breakpointList):
    parsedString = [inputString[:breakpointList[0]]]
    for i in range(0,len(breakpointList)-1):
        parsedString.append(inputString[breakpointList[i]:breakpointList[i+1]])
    searchList = []
    for x in parsedString:
        if not x == "":
            searchList.append(x)
    return searchList

def formatList(myList):
    for x in range(0,len(myList)):
        if myList[x].startswith("!tags"):
            myList[x] = myList[x][5:]
        elif myList[x].startswith("!not"):
            myList[x] = myList[x][4:]
        while myList[x].startswith(" "):
            myList[x] = myList[x][1:]
        while myList[x].endswith(" "):
            myList[x] = myList[x][:len(myList[x])-1]
        myList[x] = myList[x].replace(" ", "+")
    return myList

def findEquivalent(order):
    if order == "oldest":
        return "-date"
    elif order == "latest":
        return "%2Bdate"
    else:
        return "rank"

def findDate(date):
    dateArray = date.split("/")
    if date == dateArray[0]:
        dateArray = date.split("-")
    try:
        if len(dateArray[2]) != 4:
            if len(dateArray[2]) == 2:
                dateArray[2] = "20" + dateArray[2]
            else:
                return False
        if dateArray[0].startswith("0"):
            dateArray[0] = dateArray[0][1]
        if dateArray[1].startswith("0"):
            dateArray[1] = dateArray[1][1]
        myDate = datetime.date(int(dateArray[2]), int(dateArray[0]), int(dateArray[1]))
        today = datetime.date.today()
        firstDate = datetime.date(2003, 12, 5)
        if firstDate <= myDate <= today:
            return myDate
        else:
            return True
    except IndexError:
        return False
    except ValueError:
        return False

def resolveSearch(inputString):
    inputString = inputString.lower()
    if inputString.startswith("!wob"):
        inputString = inputString[4:]
    while inputString.startswith(" "):
        inputString = inputString[1:]
    breakpointList = breakpoints(inputString)
    breakpointList.sort()
    searchList = parseString(inputString, breakpointList)
    today = datetime.date.today()
    query, tags, antitags, before, after, speaker, order = "", "", "", "{}/{}/{}".format(today.month, today.day, today.year), "12/05/2003", "", ""
    for x in searchList:
        if not x.startswith("!"):
            query = x
            query = query.replace(" ", "+")
        elif x.startswith("!tags"):
            tags = x
        elif x.startswith("!not"):
            antitags = x
        elif x.startswith("!before"):
            before = x[7:]
            while before.startswith(" "):
                before = before[1:]
            while before.endswith(" "):
                before = before[:len(before)-1]
        elif x.startswith("!after"):
            after = x[6:]
            while after.startswith(" "):
                after = after[1:]
            while after.endswith(" "):
                after = after[:len(after)-1]
        elif x.startswith("!speaker"):
            speaker = x
            speaker = speaker.replace(" ", "+")
        elif x.startswith("!order"):
            order = x
            
    tagList = formatList(tags.split(","))
    antitagList = formatList(antitags.split(","))
    tagString = ""
    antitagString = ""
    for x in tagList:
        tagString = tagString + "&tags=" + x
    for x in antitagList:
        antitagString = antitagString + "&antitag=" + x
        
    orderEquivalent = findEquivalent(order)
    beforeDate = findDate(before)
    afterDate = findDate(after)

    #give error message
    if beforeDate == False:
        beforeDate = datetime.date.today()
    if afterDate == False:
        afterDate = datetime.date(2003, 12, 5)
    if beforeDate == True:
        beforeDate = datetime.date.today()
    if afterDate == True:
        afterDate = datetime.date(2003, 12, 5)
    if beforeDate < afterDate:
        afterDate = datetime.date(2003, 12, 5)
        beforeDate = datetime.date.today()

    #Add zeroes as needed to make YYYY-MM-DD
    if beforeDate.month < 10:
        beforeMonthString = "0" + str(beforeDate.month)
    else:
        beforeMonthString = str(beforeDate.month)
    if beforeDate.day < 10:
        beforeDayString = "0" + str(beforeDate.day)
    else:
        beforeDayString = str(beforeDate.day)
    if afterDate.month < 10:
        afterMonthString = "0" + str(afterDate.month)
    else:
        afterMonthString = str(afterDate.month)
    if afterDate.day < 10:
        afterDayString = "0" + str(afterDate.day)
    else:
        afterDayString = str(afterDate.day)
        
    beforeDate = "{}-{}-{}".format(beforeDate.year, beforeMonthString, beforeDayString)
    afterDate = "{}-{}-{}".format(afterDate.year, afterMonthString, afterDayString)
    return ("https://wob.coppermind.net/adv_search/?query={}&date_from={}&date_to={}&speaker={}{}{}&ordering={}".format(query, afterDate, beforeDate, speaker,
                                                                                                                        tagString, antitagString, orderEquivalent))
