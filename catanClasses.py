class Node:
    def __init__(self):
        self.owner = None #color, or none
        self.structure = None#city, settlement, none
        self.port = None #port type or None
        self.returns = {} #dict of num:resource, or probability of resource
        self.neighbors = {} #{neighborNode:edgeColor}

class player:
    def __init__(self, color):
        self.hand = set() #resouce cards
        self.cards = [] #development cards
        self.color = color #player color
        self.nodes = {} #(x,y):node
        self.edges = [] #do we need this?
        self.victoryPoints = 0 #can contain decimals to represent probability

class catanBoard:
    def __init__(self):
        self.nodelist = {} #location:node. 54 total nodes
        self.edgelist = {} #edgename:color ??
        self.players = {} #color:player
        self.deck = [] #stack of dev cards

    def addNode(self,location):
        self.nodelist[location] = Node()
        
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


#tileList given left->right top->bottom
tileList = [('ore', 10), ('wool', 2), ('lumber', 9), ('grain', 12), ('brick', 6), ('wool', 4), ('brick', 10), ('grain', 9), ('lumber', 11), ('desert', 0), ('lumber', 3), ('ore', 8), ('lumber', 8), ('ore', 3), ('grain', 4), ('wool', 5), ('brick', 5), ('grain', 6), ('wool', 11)]
myboard = catanBoard()
myboard.setTerrain(tileList)
for node in myboard.nodelist.values():
    print(node.returns)
