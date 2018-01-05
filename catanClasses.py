class Node:
    def __init__(self):
        self.owner #color, or none
        self.structure #city, settlement, none
        self.returns = {} #dict of num:resource, or probability of resource
        self.neighbors = {} #{neighborNode:edgeColor}

class player:
    def __init__(self, color):
        self.hand = set() #resouce cards
        self.cards = [] #development cards
        self.color = color #player color
        self.nodes = [] #do we need this?
        self.edges = [] #do we need this?
        self.victoryPoints = 0 #can contain decimals to represent probability

class catanBoard:
    def __init__(self):
        self.nodelist = {} #location:node
        self.edgelist = {} #edgename:color ??
        self.players {} #color:player
        self.deck = [] #stack of dev cards

