# This file contains player-related classes.

from enum import Enum, unique
from collections import Counter
import re
import random


@unique
class PlayerColors(Enum):
    RED = 1
    BLUE = 2
    ORANGE = 3
    WHITE = 4
    BLACK = 5
    GREEN = 6
    BANK = 7

    def FromString(s):
        s = s.upper()
        for c in PlayerColors:
            if c.name == s:
                return c
        return False


class Player:
    def __init__(self, color):
        self.hand = Counter()  # resouce cards (initialized to 4 brick, 4 wood, 2 wool, 2 grain)
        self.cards = []  # development cards
        self.color = color  # player color
        self.victoryPoints = 0  # maybe can contain decimals to represent probability
        self.longestRoad = False
        self.largestArmy = False
        self.remaining = Counter()  # remaining roads, settlements and cities

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
        if uprompt not in ["build", "trade", "devcard", "end"]
            print("You can only build, trade, play a devcard, or end")
            continue
        else:
            break
    return uprompt


class Human(Player):
    def __init__(self, color):
        Player.__init__(self, color)

    def initPlace(self, inboard):
        validSetts = inboard.validInitSetPlace()
        setLoc = inValLoc("Location of Placed Settlement: ")
        while setLoc not in validSetts:
            setLoc = inValLoc("Location of Placed Settlement: ")
        neighbors = list(inboard.nodelist[setLoc].neighbors.keys())
        possRoads = [loc for loc in inboard.nodelist if inboard.nodelist[loc] in neighbors]
        print("Possible Road Directions: {}".format(possRoads))
        setRd = inValLoc("Location of road end: ")
        while setRd not in possRoads:
            setRd = inValLoc("Location of road end: ")
        inboard.buildSettle(self.color, setLoc)
        inboard.buildRoad(self.color, setLoc, setRd)

    def build(self, inboard):
        while True:
            uprompt = input("city, settlement, road, or devcard")
            if uprompt not in ["city", "settlement", "road", "devcard"]:
                print("can only build a city, settlement, road, or devcard")
                continue
            else:
                break
        if uprompt == "city":
            loc = inValLoc("What location? (x,y)")
            inboard.buildCity(loc)
        elif uprompt == "settlement":
            loc = inValLoc("What location? (x,y)")
            inboard.buildSettle(self.color, loc)
        elif uprompt == "road":
            fromL = inValLoc("From which location? (x,y)")
            toL = inValLoc("To which location? (x,y)")
            inboard.buildRoad(self.color, fromL, toL)
        elif uprompt == "devcard":
            #TODO

    def playTurn(self, inboard):
        print("")
        print("Current Turn: {}".format(self.color))
        roll = inValRoll("What did they roll?: ")
        inboard.payout(roll)
        action = inAction("What Action? (build, trade, devcard, end): ")
        while action != "end":
            action = inAction("What Action? (build, trade, devcard, end): ")
            if action == "build":
                self.build()
            elif action == "trade":
                self.trade()
                #TODO MAKE TRADE FUNCTION
            elif action == "devcard":
                self.playDevcard()
        print("Ending Turn")


class Computer(Player):
    def __init__(self, color):
        Player.__init__(self, color)

    def initPlace(self, inboard):
        # TODO: Make this a real function. Currently does random selection
        validSetts = inboard.validInitSetPlace()
        print("BEEP BOOP BEEP BOOP")
        print("A.A.R.O.N. IS THINKING")
        print("A.A.R.O.N. Completed Initial Placement")
        nodeChoice = random.choice(validSetts)
        neighbors = list(inboard.nodelist[nodeChoice].neighbors.keys())
        possRoads = [loc for loc in inboard.nodelist if inboard.nodelist[loc] in neighbors]
        roadChoice = random.choice(possRoads)
        inboard.buildSettle(self.color, nodeChoice)
        inboard.buildRoad(self.color, nodeChoice, roadChoice)

    def playTurn(self, inboard):  # TODO: Need to implement
        return True
