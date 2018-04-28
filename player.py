# This file contains player-related classes.

from enum import Enum
from collections import Counter
from collections import OrderedDict
import re
import ast

class PlayerColors(Enum):#ok player colors should be enums too. Everything is string rn, need to update🙄
    RED  = 1
    BLUE = 2
    ORANGE = 3
    WHITE = 4
    BLACK = 5
    GREEN = 6
    BANK = 7

class Player:
    def __init__(self, color):
        self.hand = Counter() #resouce cards (initialized to 4brick, 4wood,2wool, 2 grain)
        self.cards = [] #development cards
        self.color = color #player color
        self.victoryPoints = 0 #maybe can contain decimals to represent probability
        self.longestRoad = False
        self.largestArmy = False
        self.remaining = Counter() #remaining roads, settlements and cities

    def updateVPs(self):#do I need this function? could update for each action
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
        self.buildRoad(color,fromL,toL)
        
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
    locPat = re.compile("^\(\d{1,2},\d{1,2}\)$")
    while True:
        value = input(prompt)
        if not locPat.match(value):
            print("Sorry, format needs to be (x,y)")
            continue
        else:
            break
    return ast.literal_eval(value.replace(',',', '))

class Human(Player):
    def __init__(self, color):
        Player.__init__(self, color)

    def initPlace(self, inboard):
        setLoc = inValLoc("Location of Placed Settlement: ")
        setRd = inValLoc("Location of road end: ")
        inboard.buildSettle(self.color, setLoc)
        inboard.buildRoad(self.color, setLoc, setRd)

class Computer(Player):
    def __init__(self, color):
        Player.__init__(self, color)

    def initPlace(self, inboard):
        #TODO: Make this a real function. Currently does random selection
        nodeChoice = random.sample(inboard.nodelist)
        while nodeChoice.owner != None:
            nodeChoice = random.sample(inboard.nodelist)
        roadDir = random.sample(nodeChoice.neighbors)
        while nodeChoice.neighbors[roadDir] != None:
            roadDir = random.sample(nodeChoice.neighbors)
        inboard.buildSettle(self.color, nodeChoice)
        inboard.buildRoad(self.color, nodeChoice, roadDir)

    def playTurn(self):#need to implement
        return True
