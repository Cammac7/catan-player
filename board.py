# This file contains classes for the Catan board.

import re
from enum import Enum, unique
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
    DESERT = 0
    BRICK = 1
    GRAIN = 2
    LUMBER = 3
    ORE = 4
    WOOL = 5

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

def RollFromString(s):
    r = int(s)
    if r < 2 or r > 12:
        return None
    return r

class Node:
    def __init__(self):
        self.owner = None  # color, or none
        self.structure = 0  # 0, 1 for settlement, 2 for city none
        self.port = None  # port type or None
        self.returns = {}  # dict of num:resource, or probability of resource
        self.neighbors = {}  # {neighborNode:edgeColor}


class CatanBoard:
    def __init__(self):
        self.nodelist = {}  # location:node. 54 total nodes
        self.edgelist = {}  # edgename:color ?? or color:[(locA,locB)]
        self.players = OrderedDict()  # color:player
        self.deck = []  # stack of dev cards
        self.winner = False

    def play(self):
        # Setup
        self.setTerrain(self.buildTileList())
        self.addPorts()
        # Assign player colors
        players = input(
            "Enter color of other players in clockwise order, starting to your left "
            "(comma separated like red,white,orange): ")
        clrList = players.split(",")
        self.addPlayers(clrList)
        compColor = input("Which color am I playing as? ")
        self.players[compColor] = Computer(compColor)
        playerIndex = self.initialPlacement()
        print("Finished Initial Placement")
        # TODO Added playing of each turn
        while not self.winner:
            current_player = list(self.players.values())[
                playerIndex % len(self.players)]
            current_player.playTurn(self)
            playerIndex += 1

    def initialPlacement(self):
        print("running inital placement")
        pFirst = input("Who is first? ")
        iFirst = list(self.players.keys()).index(pFirst)
        for i in range(iFirst, iFirst + ((2 * len(self.players)) - 1)):
            current_player = list(self.players.values())[i % len(self.players)]
            print("Current Turn: Player {}".format(current_player.color))
            current_player.initPlace(self)
        return iFirst

    def buildTileList(self):
        print("""Input the resources of each of the tiles in order.
The input format is '<resource> <dice roll>', where dice roll is a number 2-12
and resource is one of the letters in the following map:

    b   brick
    g   grain
    l   lumber
    o   ore
    w   wool
    d   desert

For example, 'w 10' means the tile has a resource of wool and a dice roll of 10.
Note: The roll for desert tiles will be ignored.
Other valid inputs are:

    build     Finish inputting tiles
    undo      Undo the last inputted tile
    default   Use a default tile configuration

""")

        p = re.compile(r'(\d+)\s+(\w+)')
        tList = []
        while True:
            s = input('Next tile: ').strip()
            if s == "build":
                return tList
            elif s == "undo":
                tList.pop()
            elif s == "default":
                return [
                    ('ore', 10), ('wool', 2), ('lumber', 9), ('grain', 12), ('brick', 6),
                    ('wool', 4), ('brick', 10), ('grain', 9), ('lumber', 11), ('desert', 0),
                    ('lumber', 3), ('ore', 8), ('lumber', 8), ('ore', 3), ('grain', 4),
                    ('wool', 5), ('brick', 5), ('grain', 6), ('wool', 11)]
            else:
                match = p.match(s)
                if not match:
                    print("Invalid input: '{0}'".format(s))
                    continue
                resource = ResourceFromString(match.group(2))
                if resource is None:
                    print("Invalid resource: '{0}'".format(match.group(2)))
                    continue
                roll = 0
                if resource != Resource.DESERT:
                    roll = RollFromString(match.group(1))
                    if roll is None:
                        print("Invalid dice roll: '{0}'".format(match.group(1)))
                        continue
                print("{0} {1}".format(resource, roll))
                tList.append((resource.name.lower(), roll))

    def addPlayers(self, colorList):
        for color in colorList:
            self.players[color] = Human(color)

    def addPort(self, location, portType):
        self.nodelist[location].port = portType

    def addPorts(self):
        preset = input("To set default ports, type 'default'. Any other key for custom.  ")
        if preset == "default":
            for loc in [(2,1),(3,0),(5,0),(6,1),(10,7),(10,9),(2,15),(3,16)]:
                self.addPort(loc, "ANYTHING")
            #Sheep
            self.addPort((8,3),"WOOL")
            self.addPort((9,4),"WOOL")
            #BRICK
            self.addPort((1,4),"BRICK")
            self.addPort((1,6),"BRICK")
            #LUMBER
            self.addPort((1,10),"LUMBER")
            self.addPort((1,12),"LUMBER")
            #ORE
            self.addPort((9,12),"ORE")
            self.addPort((8,13),"ORE")
            #GRAIN
            self.addPort((5,16),"GRAIN")
            self.addPort((6,15),"GRAIN")
        else:
            for i in range(18):
                location = inValLoc("What's the location of the port node? (x,y)port. OR type 'default' to set default ports ")
                portType = input("What resource? (BRICK, ORE, ETC. OR ANYTHING)")
                # TODO gotta make "portType" convert to and check for enum
                self.addPort(location, portType)

    def payout(self, roll):
        payingNodes = [node for node in self.nodelist.values() if roll in node.returns]
        for node in payingNodes:
            owner = self.players[node.owner]
            owner.hand[node[roll]] += node.structure

    def buildDev(self, color):
        print("build dev card")
        # subtract resources, add dev card to hand

    def addNode(self, location):
        self.nodelist[location] = Node()

    def buildSettle(self, color, location):
        # this needs to use resources
        selecNode = self.nodelist[location]
        selecNode.owner = color
        selecNode.structure = 1
        player = self.players[color]
        player.victoryPoints += 1  # this is faster than running the function

    def buildCity(self, location):
        selecNode = self.nodelist[location]
        selecNode.structure = 2
        self.players[selecNode.owner].updateVPs()

    def buildRoad(self, color, fromLoc, toLoc):
        fromNode = self.nodelist[fromLoc]
        toNode = self.nodelist[toLoc]
        fromNode.neighbors[toNode] = color
        toNode.neighbors[fromNode] = color

    def validInitSetPlace(self):
        openNodes = [key for key in self.nodelist if self.nodelist[key].owner == None]
        realOptions = [loc for loc in openNodes if len([n for n in self.nodelist[loc].neighbors if n.owner!=None])==0]
        print("Possible Settlement Locations: {}".format(realOptions))
        return realOptions

    def setTerrain(self, tileList):
        # list tiles left->right and top->bottom
        # These tupes are x/y coordinates of tile centers
        tileLocs = [(3, 14), (5, 14), (7, 14),
                    (2, 11), (4, 11), (6, 11), (8, 11),
                    (1, 8), (3, 8), (5, 8), (7, 8), (9, 8),
                    (2, 5), (4, 5), (6, 5), (8, 5),
                    (3, 2), (5, 2), (7, 2)]
        for index, item in enumerate(tileList):
            tl = tileLocs[index]
            x = tl[0]
            y = tl[1]
            nodeLocs = [(x - 1, y + 1), (x, y + 2), (x + 1, y + 1),
                        (x - 1, y - 1), (x, y - 2), (x + 1, y - 1)]
            for loc in nodeLocs:
                if loc not in self.nodelist:
                    self.addNode(loc)
                self.nodelist[loc].returns[item[1]] = item[0]
                for adj in [
                        (loc[0] + 1, loc[1] - 1), (loc[0], loc[1] - 2), (loc[0] - 1, loc[1] - 1),
                        (loc[0] - 1, loc[1] + 1), (loc[0], loc[1] + 2), (loc[0] + 1, loc[1] + 1)]:
                    if adj in self.nodelist:
                        # assign adjacent neighbors
                        self.nodelist[loc].neighbors[self.nodelist[adj]] = None
