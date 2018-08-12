from enum import Enum, unique

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

@unique
class Card(Enum):
    KNIGHT = 1
    RESOURCE = 2
    ROAD_BUILDING = 3
    YEAR_OF_PLENTY = 4
    MONOPOLY = 5

    def __str__(self):
        return self.name.lower()

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

class Node:
    def __init__(self):
        self.owner = None  # color, or none
        self.structure = 0  # 0, 1 for settlement, 2 for city none
        self.port = None  # port type or None
        self.returns = {}  # dict of num:resource, or probability of resource
        self.neighbors = {}  # {neighborNode:edgeColor}

class Player:
    def __init__(self, color):
        self.color = color  # this player's color
        self.hand = Counter({Resource.BRICK:4, Resource.LUMBER:4, Resource.WOOL:2, Resource.GRAIN:2})  # the resources this player has (currently set to a default hand)
        self.unplayedCards = 0  # unplayed development cards. Should be dict of Card:probability that they have it
        self.playedCards = []  # played development cards
        self.victoryPoints = 0  # maybe can contain decimals to represent probability
        self.longestRoad = False
        self.largestArmy = False
        self.remaining = Counter()  # unplayed roads, settlements, and cities that this player has in their inventory

class Board:
    def __init__(self):
        self.nodelist = {}  # location:node. 54 total nodes
        self.edgelist = {}  # edgename:color ?? or color:[(locA,locB)]
        self.players = {}  # color:player
        self.playerorder = [] #list of colors in order of play
        self.deck = []  # stack of dev cards
        self.robberTile = (5, 8)  # The starting tile of the robber is the center desert tile.
        self.currentplayer = None
