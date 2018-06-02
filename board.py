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
class Port(Enum):
    ANYTHING = 0
    BRICK = 1
    GRAIN = 2
    LUMBER = 3
    ORE = 4
    WOOL = 5

def PortFromString(s):
    if not s:
        return None
    s = s.upper()
    for r in Port:
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
        #TODO add "isRobbered" boolean property


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
            self.printBoard()
            current_player.playTurn(self)
            playerIndex += 1

    def initialPlacement(self):
        print("running inital placement")
        pFirst = input("Who is first? ")
        iFirst = list(self.players.keys()).index(pFirst)
        for i in range(iFirst, iFirst + ((2 * len(self.players)))):
            current_player = list(self.players.values())[i % len(self.players)]
            print("Current Turn: Player {}".format(current_player.color))
            current_player.initPlace(self)
        return iFirst

    def buildTileList(self):
        print("""~~~ Tiles ~~~

Input the resources of each of the tiles in order (left to right, then top to
bottom). The input format is '<dice roll><resource>', where dice roll is a
number 2-12 and resource is one of the letters in the following map:

    b   brick
    g   grain
    l   lumber
    o   ore
    w   wool
    d   desert

For example, '10w' means the tile has a resource of wool and a dice roll of 10.
Note: The roll is necessary for desert tiles but it will be ignored.
Other valid inputs are:

    build     Finish inputting tiles
    undo      Undo the last inputted tile
    default   Use a default tile configuration

""")

        p = re.compile(r'(\d\d?)\s*(\w+)')
        tList = []
        while True:
            s = input('Next tile: ').strip()
            if s == "build":
                return tList
            elif s == "undo":
                tList.pop()
            elif s == "default":
                return [
                    (Resource.ORE, 10), (Resource.WOOL, 2), (Resource.LUMBER, 9), (Resource.GRAIN, 12), (Resource.BRICK, 6),
                    (Resource.WOOL, 4), (Resource.BRICK, 10), (Resource.GRAIN, 9), (Resource.LUMBER, 11), (Resource.DESERT, 0),
                    (Resource.LUMBER, 3), (Resource.ORE, 8), (Resource.LUMBER, 8), (Resource.ORE, 3), (Resource.GRAIN, 4),
                    (Resource.WOOL, 5), (Resource.BRICK, 5), (Resource.GRAIN, 6), (Resource.WOOL, 11)]
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
                tList.append((resource, roll))

    def addPlayers(self, colorList):
        for color in colorList:
            self.players[color] = Human(color)

    def addPort(self, location, portType):
        self.nodelist[location].port = portType

    def addPorts(self):
        print('\n~~~ Ports ~~~\n')
        s = input('Use default ports? (y/n) ').lower()
        if s == 'y':
            for loc in [(2,1),(3,0),(5,0),(6,1),(10,7),(10,9),(2,15),(3,16)]:
                self.addPort(loc, Port.ANYTHING)
            self.addPort((8,3), Port.WOOL)
            self.addPort((9,4), Port.WOOL)
            self.addPort((1,4), Port.BRICK)
            self.addPort((1,6), Port.BRICK)
            self.addPort((1,10), Port.LUMBER)
            self.addPort((1,12), Port.LUMBER)
            self.addPort((9,12), Port.ORE)
            self.addPort((8,13), Port.ORE)
            self.addPort((5,16), Port.GRAIN)
            self.addPort((6,15), Port.GRAIN)
            return
        print("""
Input the ports in order of clockwise order starting with the top left port. The
format of the location is "x,y". The format for the resource is is one of the
letters in the following map:

    b   brick
    g   grain
    l   lumber
    o   ore
    w   wool
    a   anything
""")
        for i in range(18):
            l = inValLoc('Location of port? ')
            while True:
                r = input('What resource? ')
                p = PortFromString(r)
                if p is None:
                    print("Invalid resource: '{0}'".format(r))
                    continue
                break
            self.addPort(l, p)

    def payout(self, roll):
        #TODO account for Robber
        payingNodes = [node for node in self.nodelist.values() if roll in node.returns and node.owner != None]
        print("Paying nodes: {}".format(payingNodes))
        for node in payingNodes:
            print(node.owner)
            print(node.returns)
            owner = self.players[node.owner]
            owner.hand[node.returns[roll]] += node.structure

    def buildDev(self, color):
        print("build dev card")
        player = self.players[color]
        #player.hand[]
        #TODO build dev card
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

    def p(self, s):
        x = s[0]
        y = s[1]
        node = self.nodelist[s]
        if node.owner == None:
            return "({:>2},{:>2})".format(x,y)
        else:
            ow = node.owner[:1]
            if node.structure == 2:
                ow = ow.upper()
                return "(  {}  )".format(ow)

    def validInitSetPlace(self):
        openNodes = [key for key in self.nodelist if self.nodelist[key].owner == None]
        realOptions = [loc for loc in openNodes if len([n for n in self.nodelist[loc].neighbors if n.owner!=None])==0]
        self.printBoard()
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
        for loc in self.nodelist:
            for adj in [
                    (loc[0] + 1, loc[1] - 1), (loc[0], loc[1] - 2), (loc[0] - 1, loc[1] - 1),
                    (loc[0] - 1, loc[1] + 1), (loc[0], loc[1] + 2), (loc[0] + 1, loc[1] + 1)]:
                if adj in self.nodelist:
                    # assign adjacent neighbors
                    self.nodelist[loc].neighbors[self.nodelist[adj]] = None

    def p(self, s):
        x = s[0]
        y = s[1]
        node = self.nodelist[s]
        if node.owner == None:
            return "({:>2},{:>2})".format(x,y)
        else:
            ow = node.owner[:1]
            if node.structure == 2:
                ow = ow.upper()
            return "(  {}  )".format(ow)

    def printBoard(self):
        print("""                        {}         {}         {}
                       /       \       /       \       /       \ 
                {}         {}         {}         {}
                   |               |               |               |
                   |               |               |               |
                {}         {}         {}         {}
               /       \       /       \       /       \       /       \ 
        {}         {}         {}         {}         {}
           |               |               |               |               |
           |               |               |               |               |
        {}         {}         {}         {}         {}
       /       \       /       \       /       \       /       \       /       \ 
{}         {}         {}         {}         {}         {}
  |                |               |               |               |               |
  |                |               |               |               |               |
{}         {}         {}         {}         {}         {}
       \       /       \       /       \       /       \       /       \       /
        {}         {}         {}         {}         {}
           |               |               |               |               |
           |               |               |               |               |
        {}         {}         {}         {}         {}
               \       /       \       /       \       /       \       /
                {}         {}         {}         {}
                   |               |               |               |
                   |               |               |               |
                {}         {}         {}         {}
                       \       /       \       /       \       /
                        {}         {}         {}""".format(self.p((3,16)), self.p((5,16)), self.p((7,16)), self.p((2,15)), self.p((4,15)), self.p((6,15)), self.p((8,15)), self.p((2,13)), self.p((4,13)), self.p((6,13)), self.p((8,13)), self.p((1,12)), self.p((3,12)), self.p((5,12)), self.p((7,12)), self.p((9,12)), self.p((1,10)), self.p((3,10)), self.p((5,10)), self.p((7,10)), self.p((9,10)), self.p((0,9)), self.p((2,9)), self.p((4,9)), self.p((6,9)), self.p((8,9)), self.p((10,9)), self.p((0,7)), self.p((2,7)), self.p((4,7)), self.p((6,7)), self.p((8,7)), self.p((10,7)), self.p((1,6)), self.p((3,6)), self.p((5,6)), self.p((7,6)), self.p((9,6)), self.p((1,4)), self.p((3,4)), self.p((5,4)), self.p((7,4)), self.p((9,4)), self.p((2,3)), self.p((4,3)), self.p((6,3)), self.p((8,3)), self.p((2,1)), self.p((4,1)), self.p((6,1)), self.p((8,1)), self.p((3,0)), self.p((5,0)), self.p((7,0))))
