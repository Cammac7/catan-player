# This file contains classes for the Catan board.

from player import *

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


# class CatanBoard:
#     def __init__(self):
#         self.nodelist = {}  # location:node. 54 total nodes
#         self.edgelist = {}  # edgename:color ?? or color:[(locA,locB)]
#         self.players = {}  # color:player
#         self.playerorder = [] #list of colors in order of play
#         self.deck = []  # stack of dev cards
#         self.robberTile = (5, 8)  # The starting tile of the robber is the center desert tile.
#         self.currentplayer = None
#
#     def player(self, color):
#         return self.players[color]
#
#     def play(self):
#         #self.setTerrain(self.buildTileList())
#         #self.addPorts()
#         #self.addPlayers()
#         #playerIndex = self.initialPlacement()
#
#         print('\n~~~ Start game ~~~\n')
#         while not self.winner:
#             self.printBoard()
#             p = list(self.players.values())[playerIndex % len(self.players)]
#             p.playTurn()
#             playerIndex += 1
