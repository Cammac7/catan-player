# This file contains player-related classes.

from collections import Counter
import random
import datetime

class Human(Player):
    def __init__(self, color, board):
        Player.__init__(self, color, board)

class Computer(Player):
    def __init__(self, color, board):
        Player.__init__(self, color, board)
        self.states = []    #Initialize statistics table
        self.max_moves = 10  # Max moves forward for the computer
        self.calculation_time = datetime.timedelta(seconds=30) #Set turn time
        self.wins = {}
        self.plays = {}

    def initPlace(self):
        # TODO: Make this a real function. Currently does random selection
        validSetts = self.board.validInitSetPlace()
        print("BEEP BOOP BEEP BOOP")
        print("A.A.R.O.N. IS THINKING")
        print("A.A.R.O.N. Completed Initial Placement")
        nodeChoice = random.choice(validSetts)
        neighbors = list(self.board.nodelist[nodeChoice].neighbors.keys())
        possRoads = [loc for loc in self.board.nodelist if self.board.nodelist[loc] in neighbors]
        roadChoice = random.choice(possRoads)
        self.board.buildSettle(self.color, nodeChoice)
        self.board.buildRoad(self.color, nodeChoice, roadChoice)

    def update(self, state):
        self.states.append(state)
        #take the game state, append it to the history
        pass

    def runSimulation(self):
        #play out a "random" game from the current position
        #update the statistics table with the result
        visited_states = set()
        states_copy = self.states[:]
        state = states_copy[-1]

        for t in range(self.max_moves):
            legal = self.board.legal_plays(states_copy)

            play = choice(legal)
            state = self.board.next_state(state, play)
            states_copy.append(state)

            winner = self.board.winner(states_copy)
            if winner:
                break
        pass

    def playTurn(self):
        #Calculate the best move from the current game state and return it
        # TODO: Need to implement
        # 1. Determine all possible moves
        # 2. k random games are played out to the very end, and the scores are recorded.
        # 3. The move leading to the best score is chosen.
    #define weights of moves
    #basic weight == 1
    #building a city or settlement == +10000
    #building a road ==
    # 10/(10^R), where R == (AARON's Roads/AARON's settles+cities)
    # Playing a knight == +100 if the robber is blocking AARON, +1 otherwise
    #playing a dev card = +10
        #1. Roll
        roll = inValRoll("What did AARON roll?: ")
        self.board.payout(roll)
        #2. Trade
            # trading is adventageous. We should trade as much as possible.
        #3. Build
        begin = datetime.datetime.utcnow()
        while datetime.datetime.utcnow() - begin < self.calculation_time:
            self.run_simulation()
        print("A.A.R.O.N. IS PASSING")
        pass
