from board import * CatanBoard
from player import *

class StateMachine():
    def start(self): # Returns a representation of the starting state of the game.
        initialState = CatanBoard()
        setTerrain(initialState, buildTileList())
        addPlayers(initialState)
        initialPlacement(initialState)
        initialState.currentplayer = startingPlayer
        return initialState

    def current_player(self, state):
        return state.currentplayer

    def next_state(self, state, play):
        # Takes the game state, and the move to be applied.
        # Returns the new game state.
        pass

    def legal_plays(self, state_history):
        # Takes a sequence of game states representing the full
        # game history, and returns the full list of moves that
        # are legal plays for the current player.
        pass

    def winner(self, state_history):
        # Takes a sequence of game states representing the full
        # game history.  If the game is now won, return the player
        # number.  If the game is still ongoing, return zero.  If
        # the game is tied, return a different distinct value, e.g. -1.
        pass

#Actions
def payout(state, roll):
    robbedLocs = NodeLocationsForTile(state.robberTile)
    payingLocs = [loc for loc in state.nodelist if loc not in robbedLocs and roll in state.nodelist[loc].returns and state.nodelist[loc].owner != None]
    if len(payingLocs) == 0:
        print("No Payout")
        return
    print("\nPAYOUTS")
    print("Node\tOwner\tPayout")
    payingNodes = [state.nodelist[loc] for loc in payingLocs]
    for l in payingLocs:
        node = state.nodelist[l]
        print("{}\t{}\t{} {}".format(l,node.owner,node.structure,node.returns[roll]))
        owner = state.players[node.owner]
        owner.hand[node.returns[roll]] += node.structure

def moveRobber(state, loc):
    state.robberTile = loc

def buildSettle(state, color, location):
    selecNode = state.nodelist[location]
    selecNode.owner = color
    selecNode.structure = 1
    player = state.players[color]
    player.victoryPoints += 1  # this is faster than running the function

def buildCity(state, location):
    selecNode = state.nodelist[location]
    selecNode.structure = 2
    pColor = selecNode.owner
    player = state.players[pColor]
    player.victoryPoints += 1

def buildRoad(state, color, fromLoc, toLoc):
    fromNode = state.nodelist[fromLoc]
    toNode = state.nodelist[toLoc]
    fromNode.neighbors[toNode] = color
    toNode.neighbors[fromNode] = color



#Set Terrain, given a tile list.
def setTerrain(state, tileList):
    for index, item in enumerate(tileList):
        tile = TILE_LOCATIONS[index]
        for loc in NodeLocationsForTile(tile):
            if loc not in state.nodelist:
                state.nodelist[location] = Node()
            state.nodelist[loc].returns[item[1]] = item[0]
    for loc in state.nodelist:
        for adj in [
                (loc[0] + 1, loc[1] - 1), (loc[0], loc[1] - 2), (loc[0] - 1, loc[1] - 1),
                (loc[0] - 1, loc[1] + 1), (loc[0], loc[1] + 2), (loc[0] + 1, loc[1] + 1)]:
            if adj in state.nodelist:
                # assign adjacent neighbors
                state.nodelist[loc].neighbors[state.nodelist[adj]] = None

# Build tile list. Should this be inside a class?
def buildTileList():
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

def addPorts(state):
    print('\n~~~ Ports ~~~\n')
    s = input('Use default ports? (y/n) ').lower()
    if s == 'y':
        for loc in [(2,1),(3,0),(5,0),(6,1),(10,7),(10,9),(2,15),(3,16)]:
            state.nodelist[loc].port = Port.ANYTHING
        state.nodelist[(8,3)].port = Port.WOOL
        state.nodelist[(9,4)].port = Port.WOOL
        state.nodelist[(1,4)].port = Port.BRICK
        state.nodelist[(1,6)].port = Port.BRICK
        state.nodelist[(1,10)].port = Port.LUMBER
        state.nodelist[(1,12)].port = Port.LUMBER
        state.nodelist[(9,12)].port = Port.ORE
        state.nodelist[(8,13)].port = Port.ORE
        state.nodelist[(5,16)].port = Port.GRAIN
        state.nodelist[(6,15)].port = Port.GRAIN
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
                print("Invalid resource: {0}".format(r))
                continue
            break
        state.nodelist[l].port = p

def addPlayers(state):
    print('\n~~~ Players ~~~\n')
    s = input(
        "Enter color of other players in clockwise order, starting to my left "
        "(comma separated like 'red,white,orange'): ")
    colors = [ColorFromString(c.strip()) for c in s.split(",")]
    for c in colors:
        state.players[c] = Human(c, self)
        state.playerorder.append(c)
    s = input("Which color am I playing as? ")
    c = ColorFromString(s.strip())
    state.playerorder.append(c)
    state.players[c] = Computer(c, self)

#TODO: If it's our turn
def initialPlacement(state):
    print('\n~~~ Inital placement ~~~\n')
    s = input("Who is going first? ({}): ".format(state.players.keys()))
    c = ColorFromString(s.strip())
    rotate = len(state.playerorder) - state.playerorder.index(c)
    state.playerorder = state.playerorder[-rotate:] + state.playerorder[:-rotate]
    for p in range((2 * len(state.playerorder))):
        if type(state.players[p]) is Computer:
            pass
        else:
            printBoard(state)
            print("Current Turn: Player {}".format(p))
            openNodes = [key for key in state.nodelist if state.nodelist[key].owner == None]
            validSetts = [loc for loc in openNodes if len([n for n in state.nodelist[loc].neighbors if n.owner!=None])==0]
            while True:
            setLoc = inValLoc("Location of placed settlement: ")
            if setLoc not in validSetts:
                print("Invalid settlement location.")
                continue
            break
            neighbors = list(state.nodelist[setLoc].neighbors.keys())
            possRoads = [loc for loc in state.nodelist if state.nodelist[loc] in neighbors]
            print("Possible road directions: {}".format(possRoads))
            while True:
                setRd = inValLoc("Location of road end: ")
                if setRd not in possRoads:
                    print("Invalid road location.")
                    continue
                break
            buildSettle(state, p, setLoc)
            buildRoad(state, p, setLoc, setRd)

def p(state, s):
    x = s[0]
    y = s[1]
    node = state.nodelist[s]
    if node.owner == None:
        return "({:>2},{:>2})".format(x,y)
    else:
        ow = node.owner.name.lower()[:1]
        if node.structure == 2:
            ow = ow.upper()
        return "(  {}  )".format(ow)

def printBoard(state):
    print(r"""                        {}         {}         {}
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
                    {}         {}         {}""".format(p(state,(3,16)), p(state,(5,16)), p(state,(7,16)), p(state,(2,15)), p(state,(4,15)), p(state,(6,15)), p(state,(8,15)), p(state,(2,13)), p(state,(4,13)), p(state,(6,13)), p(state,(8,13)), p(state,(1,12)), p(state,(3,12)), p(state,(5,12)), p(state,(7,12)), p(state,(9,12)), p(state,(1,10)), p(state,(3,10)), p(state,(5,10)), p(state,(7,10)), p(state,(9,10)), p(state,(0,9)), p(state,(2,9)), p(state,(4,9)), p(state,(6,9)), p(state,(8,9)), p(state,(10,9)), p(state,(0,7)), p(state,(2,7)), p(state,(4,7)), p(state,(6,7)), p(state,(8,7)), p(state,(10,7)), p(state,(1,6)), p(state,(3,6)), p(state,(5,6)), p(state,(7,6)), p(state,(9,6)), p(state,(1,4)), p(state,(3,4)), p(state,(5,4)), p(state,(7,4)), p(state,(9,4)), p(state,(2,3)), p(state,(4,3)), p(state,(6,3)), p(state,(8,3)), p(state,(2,1)), p(state,(4,1)), p(state,(6,1)), p(state,(8,1)), p(state,(3,0)), p(state,(5,0)), p(state,(7,0))))
