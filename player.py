# This file contains player-related classes.

from enum import Enum, unique
from collections import Counter
import re
import random

#TODO need to implement robber 

@unique
class Resource(Enum):
    DESERT = 0
    BRICK = 1
    GRAIN = 2
    LUMBER = 3
    ORE = 4
    WOOL = 5
    
    def __str__(self):
        return self.name.lower()

def ResourceFromString(s):
    if not s:
        return None
    s = s.upper()
    for r in Resource:
        # We accept the full name with any capitalization (e.g. 'wool', 'WOOL',
        # 'wOoL', etc.) or the first letter ('w' for WOOL).
        if r.name == s or r.name[0] == s[0]:
            return r
    return None

@unique
class DevCard(Enum):
    KNIGHT = 1
    ROAD_BUILDING = 2
    YEAR_OF_PLENTY = 3
    MONOPOLY = 4
    
    def __str__(self):
        return self.name.lower()


@unique
class Color(Enum):
    RED = 1
    BLUE = 2
    ORANGE = 3
    WHITE = 4
    BLACK = 5
    GREEN = 6
    
    def __str__(self):
        return self.name.lower()

def ColorFromString(s):
    if not s:
        return None
    s = s.upper()
    for r in Color:
        # We accept the full name with any capitalization (e.g. 'red', 'RED',
        # 'ReD', etc.).
        if r.name == s:
            return r
    return None

def inResource(prompt):
    p = re.compile(r'(\d+)\s*(\w+)')
    #TODO I think we should allow this to take JUST a resource (i.e. assume number is zero if none given)
    while True:
        s = input(prompt)
        match = p.match(s)
        if not match:
            print("Invalid resource format. Expected '<number><resource>' (like '4w' for 4 wool).")
            continue
        n = int(match.group(1))
        if n < 0:
            print("Invalid number: '{}'".format(match.group(1)))
            continue
        r = ResourceFromString(match.group(2))
        if r is None or r == Resource.DESERT:
            print("Invalid resource: '{}'".format(match.group(2)))
            continue
        break
    return (n, r)

class Player:
    def __init__(self, color):
        self.hand = Counter({Resource.BRICK:4, Resource.LUMBER:4, Resource.WOOL:2, Resource.GRAIN:2})
        self.unplayedCards = 0  # unplayed development cards. Should be dict of Card:probability that they have it
        self.playedCards = []
        self.color = color  # player color #TODO change this to ColorFromString(color) [will be repurcussions]
        self.victoryPoints = 0  # maybe can contain decimals to represent probability
        self.longestRoad = False
        self.largestArmy = False
        self.remaining = Counter()  # remaining roads, settlements and cities

    def updateVPs(self):  # do I need this function? could update for each action
        newVP = 0
        for node in self.nodes.values():
            newVP += node.structure
        for card in self.playedCards:
            if card == 'VP':
                newVP += 1
        if self.longestRoad:
            newVP += 2
        if self.largestArmy:
            newVP += 2
        self.victoryPoints = newVP

def inValLoc(prompt):
    p = re.compile(r"(\d\d?)\s*,\s*(\d\d?)")
    while True:
        s = input(prompt)
        match = p.match(s)
        if not match:
            print("Invalid format. Format must be 'x,y'")
            continue
        x = int(match.group(1))
        if x < 0 or x > 10:
            print("Invalid x coordinate. x must be in the range [0, 10].")
            continue
        y = int(match.group(2))
        if y < 0 or y > 16:
            print("Invalid y coordinate. y must be in the range [0, 16].")
            continue
        break
    return (x, y)

def inValRoll(inroll):
    while True:
        roll = int(input(inroll))
        if roll not in [2,3,4,5,6,7,8,9,10,11,12]:
            print("Sorry, not a valid dice roll")
            continue
        else:
            break
    return roll

def inAction(prompt):
    while True:
        uprompt = input(prompt)
        if uprompt not in ["build", "trade", "ask", "devcard", "end"]:
            print("You can only build, trade, ask, play a devcard, or end")
            continue
        else:
            break
    return uprompt


class Player:
    def __init__(self, color, board):
        self.color = color  # this player's color
        self.board = board  # reference to the CatanBoard object
        self.hand = Counter({Resource.BRICK:4, Resource.LUMBER:4, Resource.WOOL:2, Resource.GRAIN:2})  # the resources this player has (currently set to a default hand)
        self.unplayedCards = 0  # unplayed development cards. Should be dict of Card:probability that they have it
        self.playedCards = []  # played development cards
        self.victoryPoints = 0  # maybe can contain decimals to represent probability
        self.longestRoad = False
        self.largestArmy = False
        self.remaining = Counter()  # unplayed roads, settlements, and cities that this player has in their inventory

    def updateVPs(self):  # do I need this function? could update for each action
        newVP = 0
        for node in self.nodes.values():
            newVP += node.structure
        for card in self.cards:
            if card == 'VP':
                newVP += 1
            elif card == 'Longest Road' or card == 'Largest Army':
                newVP += 2
        self.victoryPoints = newVP


class Human(Player):
    def __init__(self, color, board):
        Player.__init__(self, color, board)

    def initPlace(self):
        validSetts = self.board.validInitSetPlace()
        setLoc = inValLoc("Location of Placed Settlement: ")
        while setLoc not in validSetts:
            setLoc = inValLoc("Location of Placed Settlement: ")
        neighbors = list(self.board.nodelist[setLoc].neighbors.keys())
        possRoads = [loc for loc in self.board.nodelist if self.board.nodelist[loc] in neighbors]
        print("Possible Road Directions: {}".format(possRoads))
        setRd = inValLoc("Location of road end: ")
        while setRd not in possRoads:
            setRd = inValLoc("Location of road end: ")
        self.board.buildSettle(self.color, setLoc)
        self.board.buildRoad(self.color, setLoc, setRd)

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
        while True:
            s = input("Who is {} trading with (enter 'maritime' for maritime trades)?: ".format(self.color)).strip()
            if s.lower() == "maritime":
                maritime = True
                break
            c = ColorFromString(s)
            if c is None or c not in self.board.players:
                print("Invalid color.")
                continue
            break
        if maritime:
            port = False
            s = input('Is the trade at a port? i.e 3:1. (y/n) ').lower()
            giving = ResourceFromString(input("What is {} trading? (b/g/l/o/w): ".format(self.color)))
            getting = ResourceFromString(input("What is {} receiving? (b/g/l/o/w): ".format(self.color)))
            if s == "y":
                self.hand.subtract({giving:3})
                self.hand += {getting:1}
            else:
                self.hand.subtract({giving:4})
                self.hand += {getting:1}
        else:
            nSelf, rSelf = inResource("What is {} trading?: ".format(self.color))
            nThem, rThem = inResource("What is {} trading?: ".format(c.name.lower()))
            otherPlayer = self.board.players[c]
            giving = {rSelf:nSelf}
            getting = {rThem:nThem}
            self.hand.subtract(giving)
            self.hand += getting
            otherPlayer.hand.subtract(getting)
            otherPlayer.hand += giving
            # TODO

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
            #TODO add robber moves
        elif dcard == "Road Building":
            for n in range(3):
                print("Segment {}/3".format(n+1))
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
        print("")
        print("Current Turn: {}".format(self.color))
        roll = inValRoll("What did they roll?: ")
        self.board.payout(roll)
        action = inAction("What Action? (build, trade, devcard, end): ")
        while action != "end":
            if action == "build":
                self.build()
            elif action == "trade":
                self.trade()
            elif action == "devcard":
                self.playDevcard()
            #TODO add check board state for longest road/largest army. (and winner?)
            action = inAction("What Action? (build, trade, devcard, end): ")
        print("Ending Turn")


class Computer(Player):
    def __init__(self, color, board):
        Player.__init__(self, color, board)

    def initPlace(self):
        # TODO: Make this a real function. Currently does random selection
        validSetts = self.board.validInitSetPlace()
        print("BEEP BOOP BEEP BOOP")
        print("A.A.R.O.N. IS THINKING")
        print("A.A.R.O.N. Completed Initial Placement")
        nodeChoice = random.choice(validSetts)
        neighbors = list(self.board.nodelist[nodeChoice].neighbors.keys())
        possRoads = [loc for loc in self.board.nodelist if self.board.nodelist[loc] in neighbors]
        roadChoice = random.choice(possRoads)
        self.board.buildSettle(self.color, nodeChoice)
        self.board.buildRoad(self.color, nodeChoice, roadChoice)

    def playTurn(self):
        # TODO: Need to implement
        pass
