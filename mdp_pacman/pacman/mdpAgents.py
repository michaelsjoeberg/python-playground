# mdpAgents.py

from pacman import Directions
from game import Agent
import api
import random
import game
import util
import copy

### IMPORTANT ---------------------------------------

# conda create --name <environment_name> python=2.7
# source activate <environment_name>

### IMPORTANT ---------------------------------------

DEBUG = False

# python pacman.py -p MDPAgent -l smallGrid
# python pacman.py -p MDPAgent -l mediumClassic
# python pacman.py -q -n 10 -p MDPAgent -l smallGrid
# python pacman.py -q -n 10 -p MDPAgent -l mediumClassic

class MDPAgent(Agent):

    def __init__(self):
        self.map = { 'states': {} }
        self.moves = {
            Directions.WEST: (-1, 0),
            Directions.EAST: (1, 0), 
            Directions.NORTH: (0, 1),
            Directions.SOUTH: (0, -1)
        }

        # variables
        self.utility_food = 1
        self.utility_food_in_direction = self.utility_food
        self.utility_ghost = -1
        self.utility_ghost_in_direction = self.utility_ghost
        self.ghost_timer_limit = 10

    def registerInitialState(self, state):
        
        pass

    def final(self, state):
        # reset self
        del self.map
        del self.moves
        del self.utility_food
        del self.utility_food_in_direction
        del self.utility_ghost
        del self.utility_ghost_in_direction
        del self.ghost_timer_limit

        self.__init__()

    def get_average_expected_utility(self, location, iteration):
        '''Function to get average expected utility for a state and neighbors (deterministic 
        approximation), using average to account for negative ghost utility (pacman should 
        avoid states close to ghost).
        '''

        # sanity check
        if location not in iteration: return -1

        # add utility at current location
        expected_utility = []
        expected_utility.append(iteration[location]['utility'])

        # get utility from each next move
        for move in self.moves.keys():
            transition = self.moves[move]

            # define next_state
            next_state = (location[0] + transition[0], location[1] + transition[1])

            # add utility at next location (unless not valid state)
            if (next_state in iteration): expected_utility.append(iteration[next_state]['utility'])

        return sum(expected_utility) / len(expected_utility)

    def value_iteration(self, MAX_ITERATIONS=100, DISCOUNT_VALUE=0.9, REWARD=-0.02):
        '''Function to iterate maps until utility in states no longer change, using average 
        expected utility, and skipping states with food and ghosts.'''

        # append copy of initial state to map_iterations
        map_iterations = [] 
        map_iterations.append(copy.deepcopy(self.map['states']))

        n = 0
        while (n < MAX_ITERATIONS):
            n += 1

            # append copy of previous iteration to map_iterations
            map_iterations.append(copy.deepcopy(map_iterations[n - 1]))

            # iterate each location in previous iteration
            for location in map_iterations[n - 1]:
                if (not map_iterations[n - 1][location]['food'] and 
                    not map_iterations[n - 1][location]['ghost']):

                    # calculate utility in previous iteration and add to corresponding location in current iteration
                    map_iterations[n][location]['utility'] = round(REWARD + (DISCOUNT_VALUE * self.get_average_expected_utility(location, map_iterations[n - 1])), 3)
            
            if (map_iterations[n - 1] == map_iterations[n]):
                # set final state of map 
                self.map['states'] = map_iterations[n]
                return 1

        return -1

    def set_food_utility(self, state, legal):
        '''Function to set utility in states with food.'''

        foods = api.food(state)

        # set utility in states with food
        for food in foods: 
            if food in self.map['states']:
                self.map['states'][food]['food'] = True
                self.map['states'][food]['utility'] = self.utility_food

                # set utility in states with food in direction
                for move in legal:
                    if (api.inFront(food, move, state)): self.map['states'][food]['utility'] = self.utility_food_in_direction

        # find all states with food
        food_in_map = [location for location in self.map['states'].keys() if self.map['states'][location]['food'] == True]
        for food in food_in_map:
            # unless last food in map
            if (len(food_in_map) > 1):
                next_state_walls = []
                for move in self.moves.keys():
                    transition = self.moves[move]

                    # define next_state
                    next_state = (food[0] + transition[0], food[1] + transition[1])

                    if (next_state not in self.map['states']): 
                        next_state_walls.append(True)
                    else:
                        next_state_walls.append(False)

                    # hide food in state that is dead end
                    if (next_state_walls.count(True) == 3):
                        self.map['states'][food]['food'] = False
                        self.map['states'][food]['utility'] = 0

        return 1

    def set_ghost_utility(self, state, legal):
        '''Function to set utility in states with ghost.'''

        ghosts = api.ghostStatesWithTimes(state)

        # set utility in states with ghost
        for ghost in ghosts:
            location = (int(ghost[0][0]), int(ghost[0][1]))

            if location in self.map['states']:
                # ghosts are scared
                if (ghost[1] > self.ghost_timer_limit):
                    # set ghost to true but ignore
                    self.map['states'][location]['ghost'] = True
                # otherwise
                else:
                    # set utility in states with ghost
                    self.map['states'][location]['ghost'] = True
                    self.map['states'][location]['danger'] = True
                    self.map['states'][location]['utility'] = self.utility_ghost

                    # set utility in states with ghost in direction
                    for move in legal:
                        if (api.inFront(location, move, state)): 
                            self.map['states'][location]['utility'] = self.utility_ghost_in_direction

                    # set utility in states near state with ghost
                    self.set_ghost_padding(location, 0, len(ghosts))

        return 1

    def set_ghost_padding(self, location, N, N_MAX=10):
        '''Function to recursively add padding to states near ghost.'''

        # sanity check
        if (N < N_MAX):
            for move in self.moves.keys():
                transition = self.moves[move]

                # define next location
                next_location = (location[0] + transition[0], location[1] + transition[1])

                # next_location in available states (i.e. not a wall)
                if (next_location in self.map['states']):
                    if (not self.map['states'][next_location]['ghost']):
                        # set utility in next_location
                        self.map['states'][next_location]['danger'] = True
                        self.map['states'][next_location]['utility'] = self.utility_ghost

                self.set_ghost_padding(next_location, N + 1, N_MAX)

    def create_map(self, state, legal):
        '''Function to create map.'''

        corners = api.corners(state)
        walls = api.walls(state)
        pacman = api.whereAmI(state)

        # create empty states between corners in map
        for i in range(corners[3][0]):
            for j in range(corners[3][1]):
                location = (i, j)

                self.map['states'][location] = { 
                    'location': location, 
                    'ghost': False, 
                    'danger': False, 
                    'food': False, 
                    'visited': False, 
                    'utility': 0 }

        # delete location of walls from states
        for wall in walls:
            if wall in self.map['states']: del self.map['states'][wall]

        self.set_food_utility(state, legal)

        self.set_ghost_utility(state, legal)

        # override pacman location
        self.map['states'][pacman]['ghost'] = False
        self.map['states'][pacman]['food'] = False
        self.map['states'][pacman]['utility'] = 0

        return self.value_iteration()

    def get_best_move(self, location, iteration):
        '''Function to get best move in location and iteration.'''

        # sanity check
        if location not in iteration: return -1

        # get utility resulting from each next move
        utility_lst = []
        for move in self.moves.keys():
            transition = self.moves[move]

            # define next_state
            next_state = (location[0] + transition[0], location[1] + transition[1])

            # add utility and move at next location (unless not valid state)
            if (next_state in iteration): utility_lst.append((iteration[next_state]['utility'], move))

        if (DEBUG): 
            print(sorted(utility_lst, key=lambda utility: -utility[0]))
            print('---')

        return max(sorted(utility_lst, key=lambda utility: -utility[0]))[1]

    def getAction(self, state):
        legal = api.legalActions(state)
        pacman = api.whereAmI(state)

        if Directions.STOP in legal: legal.remove(Directions.STOP)

        # create map (at each move to reflect changing environment)
        self.create_map(state, legal)

        ### TEST --------------------------------------------
        if (DEBUG):
            map_sorted = sorted(self.map['states'], key=lambda location: -self.map['states'][location]['utility'])
            for location in map_sorted:
                if (self.map['states'][location]['location'] == pacman):
                    print(str(self.map['states'][location]['location']) + ": " + str(self.map['states'][location]['utility']) + "\t - Pacman")
                elif (self.map['states'][location]['ghost']):
                    print(str(self.map['states'][location]['location']) + ": " + str(self.map['states'][location]['utility']) + "\t - Ghost")
                elif (self.map['states'][location]['danger']):
                    print(str(self.map['states'][location]['location']) + ": " + str(self.map['states'][location]['utility']) + "\t - Danger")
                else:
                    print(str(self.map['states'][location]['location']) + ": " + str(self.map['states'][location]['utility']))
            print('---')
        ### TEST --------------------------------------------

        return api.makeMove(self.get_best_move(pacman, self.map['states']), legal)
