def roll(self):
    roll = inValRoll("What did they roll?: ")
    if roll != 7:
        self.board.payout(roll)
        return
    # Robber time
    # TODO: Every player's hand that is > 7 cards loses half their hand, rounded down.
    self.moveRobber()

def moveRobber(self):
    loc = inValLoc("Where are you moving the robber? (x,y): ")
    self.board.moveRobber(loc)
    c = inPlayerColor("Which player is being stolen from?: ", self.board.players)
    _, r = inResource("What resource was taken?: ") # TODO: This should actually be secret/unknown to the AI
    self.board.players[c].hand.subtract({r:1})
    self.hand += {r:1}

def build(self):
    while True:
        uprompt = input("city, settlement, road, or devcard?: ")
        if uprompt not in ["city", "settlement", "road", "devcard"]:
            print("can only build a city, settlement, road, or devcard")
            continue
        else:
            break
    if uprompt == "city":
        loc = inValLoc("What location? (x,y)")
        city = {Resource.ORE:3, Resource.GRAIN:2}
        self.hand.subtract(city)
        self.board.buildCity(loc)
    elif uprompt == "settlement":
        loc = inValLoc("What location? (x,y)")
        settlement = {Resource.BRICK:1, Resource.LUMBER:1, Resource.WOOL:1, Resource.GRAIN:1}
        self.hand.subtract(settlement)
        self.board.buildSettle(self.color, loc)
    elif uprompt == "road":
        fromL = inValLoc("From which location? (x,y)")
        toL = inValLoc("To which location? (x,y)")
        road = {Resource.BRICK:1, Resource.LUMBER:1}
        self.hand.subtract(road)
        self.board.buildRoad(self.color, fromL, toL)
    elif uprompt == "devcard":
        devcard = {Resource.ORE:1, Resource.GRAIN:1, Resource.WOOL:1}
        self.hand.subtract(devcard)
        self.unplayedCards += 1

def trade(self):
    p = re.compile(r'(\d+)\s*(\w+)')
    maritime = False
    s = input("Is this a maritime trade (i.e. a trade with the bank)? (y/n): ").strip().lower()
    if s == "y":
        port = False
        s = input("Is the trade at a port (i.e. 3:1)? (y/n): ").lower()
        giving = ResourceFromString(input("What is {} trading? (b/g/l/o/w): ".format(self.color)))
        getting = ResourceFromString(input("What is {} receiving? (b/g/l/o/w): ".format(self.color)))
        if s == "y":
            self.hand.subtract({giving:3})
            self.hand += {getting:1}
        else:
            self.hand.subtract({giving:4})
            self.hand += {getting:1}
    else:
        c = inPlayerColor("Which player is {} trading with?: ".format(self.color), self.board.players)
        nSelf, rSelf = inResource("What is {} trading?: ".format(self.color))
        nThem, rThem = inResource("What is {} trading?: ".format(c.name.lower()))
        otherPlayer = self.board.players[c]
        giving = {rSelf:nSelf}
        getting = {rThem:nThem}
        self.hand.subtract(giving)
        self.hand += getting
        otherPlayer.hand.subtract(getting)
        otherPlayer.hand += giving

def playDevcard(self):
    while True:
        dcard = input("What card? Knight, Road Building, Year of Plenty, or Monopoly: ")
        if dcard not in ["Knight", "Road Building", "Year of Plenty", "Monopoly"]:
            print("can only play a Knight, Road Building, Year of Plenty, or Monopoly")
            continue
        else:
            break
    if dcard == "Knight":
        self.unplayedCards -= 1
        self.playedCards.append(DevCard.KNIGHT)
        self.moveRobber()
    elif dcard == "Road Building":
        for n in range(2):
            print("Segment {}/2".format(n+1))
            fromL = inValLoc("From which location? (x,y): ")
            toL = inValLoc("To which location? (x,y): ")
            self.board.buildRoad(self.color, fromL, toL)
    elif dcard == "Year of Plenty":
        num, resource = inResource("Which resource was selected?: ")
        while True:
            if num == 1:
                self.hand += {resource:num}
                num, resource = inResource("Which resource was selected?: ")
                self.hand += {resource:num}
                break
            elif num == 2:
                self.hand += {resource:num}
                break
            else:
                continue
    elif dcard == "Monopoly":
        num, resource = inResource("Which resource was selected?: ")
        for player in self.board.players.values():
            if player != self:
                amount = player.hand[resource]
                self.hand += {resource:amount}
                player.hand[resource] = 0   
    #TODO "We should make these Enums" - Mark Langer probably

def playTurn(self):
    # TODO: Announcing whose turn it is and rolling should be part of they
    # base Player class, since that has to happen for any player, human or not.
    print("")
    print("Current Turn: {}".format(self.color))
    self.roll()
    actionPrompt = "What Action? (build, trade, devcard, end): "
    action = inAction(actionPrompt)
    while action != "end":
        if action == "build":
            self.build()
        elif action == "trade":
            self.trade()
        elif action == "devcard":
            self.playDevcard()
        #TODO add check board state for longest road/largest army. (and winner?)
        action = inAction(actionPrompt)
    print("Ending Turn")