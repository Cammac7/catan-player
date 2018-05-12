# This file contains player-related classes.

from enum import Enum, unique
from collections import Counter
from collections import OrderedDict
import re
import ast
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

    def buildRoad(self):
        color = input("Which color player?")
        fromL = inValLoc("From which location? (x,y)")
        toL = inValLoc("To which location? (x,y)")
        self.buildRoad(color, fromL, toL)

    def buildCity(self):
        loc = inValLoc("What location? (x,y)")
        self.buildCity(loc)

    def buildDev(self):
        color = input("Which color player?")

    def buildSettle(self):
        color = input("Which color player?")
        loc = inValLoc("What location? (x,y)")
        self.buildSettle(color, loc)


def inValLoc(prompt):
    locPat = re.compile(r"^\(\d{1,2},\d{1,2}\)$")
    while True:
        value = input(prompt)
        if not locPat.match(value):
            print("Sorry, format needs to be (x,y)")
            continue
        else:
            break
    return ast.literal_eval(value.replace(',', ', '))


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

class Computer(Player):
    def __init__(self, color):
        Player.__init__(self, color)

    def initPlace(self, inboard):
        # TODO: Make this a real function. Currently does random selection
        validSetts = inboard.validInitSetPlace()
        nodeChoice = random.choice(validSetts)
        neighbors = list(inboard.nodelist[nodeChoice].neighbors.keys())
        possRoads = [loc for loc in inboard.nodelist if inboard.nodelist[loc] in neighbors]
        roadChoice = random.choice(possRoads)
        inboard.buildSettle(self.color, nodeChoice)
        inboard.buildRoad(self.color, nodeChoice, roadChoice)

    def playTurn(self):  # TODO: Need to implement
        return True
