# This file contains classes for the Catan board.

import re
from enum import Enum, unique
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
    
    def __str__(self):
        return self.name.lower()

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

# TILE_LOCATIONS lists tiles left->right and top->bottom.
# These tupes are x/y coordinates of tile centers.
TILE_LOCATIONS = [
    (3, 14), (5, 14), (7, 14),
    (2, 11), (4, 11), (6, 11), (8, 11),
    (1, 8), (3, 8), (5, 8), (7, 8), (9, 8),
    (2, 5), (4, 5), (6, 5), (8, 5),
    (3, 2), (5, 2), (7, 2)
]

def NodeLocationsForTile(tile):
    x = tile[0]
    y = tile[1]
    return [(x - 1, y + 1), (x, y + 2), (x + 1, y + 1), (x - 1, y - 1), (x, y - 2), (x + 1, y - 1)]


class CatanBoard:
    def __init__(self):
        self.nodelist = {}  # location:node. 54 total nodes
        self.edgelist = {}  # edgename:color ?? or color:[(locA,locB)]
        self.players = {}  # color:player
        self.playerorder = [] #list of colors in order of play
        self.deck = []  # stack of dev cards
        self.robberTile = (5, 8)  # The starting tile of the robber is the center desert tile.
        self.currentplayer = None

    def player(self, color):
        return self.players[color]

    def play(self):
        #self.setTerrain(self.buildTileList())
        #self.addPorts()
        #self.addPlayers()
        #playerIndex = self.initialPlacement()
        
        print('\n~~~ Start game ~~~\n')
        while not self.winner:
            self.printBoard()
            p = list(self.players.values())[playerIndex % len(self.players)]
            p.playTurn()
            playerIndex += 1


