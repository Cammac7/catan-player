class Card(Enum):
    KNIGHT = 1
    RESOURCE = 2
    ROAD_BUILDING = 3
    YEAR_OF_PLENTY = 4
    MONOPOLY = 5

class Resource(Enum):
    ORE = 1
    BRICK = 2
    GRAIN = 3 
    LUMBER = 4
    WOOL = 5

class PlayerColors(Enum):#ok player colors should be enums too. Everything is string rn, need to update🙄
    RED  = 1
    BLUE = 2
    ORANGE = 3
    WHITE = 4
    BLACK = 5
    GREEN = 6
    BANK = 7

class Node: 
    def __init__(self):
        self.owner = None #color, or none
        self.structure = 0#0, 1 for settlement,2 for city none
        self.port = None #port type or None
        self.returns = {} #dict of num:resource, or probability of resource
        self.neighbors = {} #{neighborNode:edgeColor}


class Player:
    def __init__(self, color):
        self.hand = Counter() #resouce cards (initialized to 4brick, 4wood,2wool, 2 grain)
        self.cards = [] #development cards
        self.color = color #player color
        self.victoryPoints = 0 #maybe can contain decimals to represent probability
        self.remaining = {} #remaining roads, settlements and cities
        self.longestRoad = false
        self.largestArmy = false
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

    def initialTurn(self):
        raise Exception("Not Implemented")


class Human(Player):
    def __init__(self, color):
        Player.__init__(self, color)

class Computer(Player):
    def __init__(self, color):
        Player.__init__(self, color)

    def playTurn():#need to implement
        return True

class CatanBoard:
    def __init__(self):
        self.nodelist = {} #location:node. 54 total nodes
        self.edgelist = {} #edgename:color ?? or color:[(locA,locB)]
        self.players = {} #color:player
        self.deck = [] #stack of dev cards
        self.winner = False

    def play():
    #Setup
        self.setTerrain(self.buildTileList())
        #Assign player colors
        players = input("Enter color of other players in clockwise order, starting to your left (comma separated like red,white,orange): )")
        clrList = players.split(",")
        self.addPlayers(clrList)
        compColor = input("Which color am I playing as? ")
        self.players[compColor] = Player(compColor)
        self.initialPlacement()
        function_mappings = {
                'initial placement': initalPlacement(),
                'build settlement': userBuildSettle(),
                'build city': userBuildCity(),
                'build road': userBuildRoad(),
                'build dev card': userBuildDev(),
                'make trade': None,
                'monopoly' : None,
                'year of plenty' : None,
                'knight': None,
                'road building': None
                'roll' : userRoll(diceTotal) #not yet implemented. Gonna want to parse string and pass val like "roll 10"
                'play turn': None
                }
        while winner == False:
           winner = True #this is where we'll run the game 
           #take input, map it to a function using the above
           #when computer's turn, call play turn, execute computer turn

    def initialPlacement():
        pColor = input("Who is placing?")
        setLoc = input("Location of Placed Settlement: ")
        setRd = input("Location of road end: ")
        #If color == computer then run our initial placement function
        self.buildSettle(pColor,setLoc)
        self.buildRoad(pColor,setLoc,setRd)
    
    def hello():
        print("Hellloooo!!")

    def buildTileList():
        tList = []
        lMap = {'g':'grain','b':'brick','o':'ore','l':'lumber','w':'wool','d':'dese    rt'}
        while True:
            com = input('Next Tile:')
            if com == "build":
                return tList
            if com == "undo":
                tList.pop()
            else:
                resource = lMap[com[-1:]]
                number = int(com[0:-1])
                tList.append((resource,number))

    def addPlayers(colorList):
        for color in colorList:
            self.players[color] = Player(color)
    
    def userAddPort():
        location = input("What's the location of the node?")
        portType = input("What resource? (BRICK, ORE, ETC. OR ANYTHING)")
        self.addPort(location,portType)
    def addPort(self,location,portType):
        self.nodelist[location].port = portType

    def addNode(self,location):
        self.nodelist[location] = Node()

    def userBuildSettle():
        color = input("Which color player?")
        loc = input("What location? (x,y)")
        self.buildSettle(color, loc)
    def buildSettle(self,color,location):
        #this needs to use resources
        selecNode = self.nodelist[location]
        selecNode.owner = color
        selecNode.structure = 1
        player = self.players[color]
        player.victoryPoints += 1 #this is faster than running the function

    def userBuildCity():
        loc = input("What location? (x,y)")
        self.buildCity(loc)
    def buildCity(self, location):
        selecNode = self.nodelist[location]
        selecNode.structure = 2
        self.players[selecNode.owner].updateVPs()

    def userBuildRoad():
        color = input("Which color player?")
        fromL = input("From which location? (x,y)")
        toL = input("To which location? (x,y)")
        self.buildRoad(color,fromL,toL)
    def buildRoad(self, color, fromLoc, toLoc):
        fromNode = nodelist[fromLoc]
        toNode = nodelist[toLoc]
        fromNode.neighbors[toNode] = color
        toNode.neighbors[fromNode] = color

    def userBuildDev():
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


#tileList given left->right top->bottom
tileList = [('ore', 10), ('wool', 2), ('lumber', 9), ('grain', 12), ('brick', 6), ('wool', 4), ('brick', 10), ('grain', 9), ('lumber', 11), ('desert', 0), ('lumber', 3), ('ore', 8), ('lumber', 8), ('ore', 3), ('grain', 4), ('wool', 5), ('brick', 5), ('grain', 6), ('wool', 11)]
myboard = CatanBoard()
myboard.play()
#myboard.setTerrain(tileList)
#for node in myboard.nodelist.values():
#    nears = [nb.returns for nb in node.neighbors.keys()]
#    print("Node is: {}. Node neighb is: {}".format(node.returns, nears))
