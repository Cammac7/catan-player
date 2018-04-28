# This file contains classes for the Catan board.

import re
import ast
from enum import Enum, unique
from collections import Counter
from collections import OrderedDict
from player import *

@unique
class Card(Enum):
    KNIGHT = 1
    RESOURCE = 2
    ROAD_BUILDING = 3
    YEAR_OF_PLENTY = 4
    MONOPOLY = 5

    def FromString(s):
        s = s.upper()
        for c in Card:
            if c.name == s:
                return c
        return False

@unique
class Resource(Enum):
    ORE = 1
    BRICK = 2
    GRAIN = 3
    LUMBER = 4
    WOOL = 5

    def FromString(s):
        s = s.upper()
        for r in Resource:
            if r.name == s:
                return r
        return False

class Node:
    def __init__(self):
        self.owner = None #color, or none
        self.structure = 0#0, 1 for settlement,2 for city none
        self.port = None #port type or None
        self.returns = {} #dict of num:resource, or probability of resource
        self.neighbors = {} #{neighborNode:edgeColor}

class CatanBoard:
    def __init__(self):
        self.nodelist = {} #location:node. 54 total nodes
        self.edgelist = {} #edgename:color ?? or color:[(locA,locB)]
        self.players = OrderedDict() #color:player
        self.deck = [] #stack of dev cards
        self.winner = False

    def play(self):
    #Setup
        self.setTerrain(self.buildTileList())
        #Assign player colors
        players = input("Enter color of other players in clockwise order, starting to your left (comma separated like red,white,orange): )")
        clrList = players.split(",")
        self.addPlayers(clrList)
        compColor = input("Which color am I playing as? ")
        self.players[compColor] = Computer(compColor)
        self.initialPlacement()
        print("Finished Initial Placement")
        #TODO Added playing of each turn

    def initialPlacement(self):
        print("running inital placement")
        pFirst = input("Who is first? ")
        iFirst = list(self.players.keys()).index(pFirst)
        for i in range(iFirst, iFirst+((2*len(self.players))-1)):
            current_player = list(self.players.values())[i]
            current_player.initPlace(self)

    def buildTileList(self):
        tList = []
        lMap = {'g':'grain','b':'brick','o':'ore','l':'lumber','w':'wool','d':'desert'}
        while True:
            com = input('Next Tile:')
            if com == "build":
                return tList
            if com == "undo":
                tList.pop()
            if com == "default":
                tList = [('ore',10),('wool',2),('lumber',9),('grain',12),('brick',6),('wool',4),('brick',10),('grain',9),('lumber',11),('desert',0),('lumber',3),('ore',8),('lumber',8),('ore',3),('grain',4),('wool',5),('brick',5),('grain',6),('wool',11) ]
                return tList
            else:
                resource = lMap.get(com[-1:],'desert')
                number = int(com[0:-1])
                tList.append((resource,number))

    def addPlayers(self,colorList):
        for color in colorList:
            self.players[color] = Human(color)

    def userAddPort(self):
        location = inValLoc("What's the location of the node? (x,y) ")
        portType = input("What resource? (BRICK, ORE, ETC. OR ANYTHING)")
        self.addPort(location,portType)
    def addPort(self,location,portType):
        self.nodelist[location].port = portType

    def addNode(self,location):
        self.nodelist[location] = Node()

    def userBuildSettle(self):
        color = input("Which color player?")
        loc = inValLoc("What location? (x,y)")
        self.buildSettle(color, loc)
    def buildSettle(self,color,location):
        #this needs to use resources
        selecNode = self.nodelist[location]
        selecNode.owner = color
        selecNode.structure = 1
        player = self.players[color]
        player.victoryPoints += 1 #this is faster than running the function

    def userBuildCity(self):
        loc = inValLoc("What location? (x,y)")
        self.buildCity(loc)
    def buildCity(self, location):
        selecNode = self.nodelist[location]
        selecNode.structure = 2
        self.players[selecNode.owner].updateVPs()

    def userBuildRoad(self):
        color = input("Which color player?")
        fromL = inValLoc("From which location? (x,y)")
        toL = inValLoc("To which location? (x,y)")
        self.buildRoad(color,fromL,toL)
    def buildRoad(self, color, fromLoc, toLoc):
        fromNode = self.nodelist[fromLoc]
        toNode = self.nodelist[toLoc]
        fromNode.neighbors[toNode] = color
        toNode.neighbors[fromNode] = color

    def userBuildDev(self):
        color = input("Which color player?")
    def buildDev(self, color):
        print("build dev card")
        #subtract resources, add dev card to hand

    def setTerrain(self,tileList):
        #list tiles left->right and top->bottom
        #These tupes are x/y coordinates of tile centers
        tileLocs = [(3,14),(5,14),(7,14),
                    (2,11),(4,11),(6,11),(8,11),
                    (1,8),(3,8),(5,8),(7,8),(9,8),
                    (2,5),(4,5),(6,5),(8,5),
                    (3,2),(5,2),(7,2)]
        for index, item in enumerate(tileList):
            tl = tileLocs[index]
            x = tl[0]
            y = tl[1]
            nodeLocs = [(x-1,y+1),(x,y+2),(x+1,y+1),(x-1,y-1),(x,y-2),(x+1,y-1)]
            for loc in nodeLocs:
                if loc not in self.nodelist:
                    self.addNode(loc)
                self.nodelist[loc].returns[item[1]] = item[0]
                for adj in [(loc[0]+1,loc[1]-1),(loc[0],loc[1]-2),(loc[0]-1,loc[1]-1),(loc[0]-1,loc[1]+1),(loc[0],loc[1]+2),(loc[0]+1,loc[1]+1)]:
                    if adj in self.nodelist:
                        self.nodelist[loc].neighbors[self.nodelist[adj]] = None #assign adjacent neighbors

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
