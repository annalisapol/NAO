# This file defines the NAOProblem class used for search-based planning.
# It encodes the robot's possible moves, constraints, and how states
# transition during the choreography planning 
from search import Problem
from constants import MOVES, MAX_TIME
from moves_helpers import (
    get_mandatory_moves,
    get_intermediate_moves)

from utils import distance

class NAOProblem(Problem):
    def __init__(self, max_time=MAX_TIME, initial_state=None, goal=None):
        '''
        Initialize the planning problem with:
        - Initial state
        - Goal conditions
        - Durations of each move
        - Incompatibility constraints
        - Maximum allowed time (2 min = 120s)
        '''
        self.MANDATORY = set(get_mandatory_moves())
        self.INTERMEDIATE = set(get_intermediate_moves())

        self.state={
            "time": 0,
            #copying the mandatory moves set to avoid modifying the global structure
            "mandatory_left": self.MANDATORY.copy(),
            "intermediate_count":0,
            "posture": "None",
            # changing this to None because "Stand" still needs to be computed, since time is at 0
            # initial posture is not defined yet 
            # "Stand" should be passed to the problem in some way and then compute it's time
            
            # keeping track of moves done for forcing initial and final postures
            "moves_done": []
        }
        
        super().__init__(self.state,None)

        self.max_time = max_time
        
    # changing name into actions otherwise it won't override the Problem "actions" class method
    def actions(self, state):
        '''
        Return all possible moves that the robot can execute from the current states
        This applies filters for:
        - Time limit 
        - Incompatibilities with previous move
        - Posture requirements (standing/sitting)
        '''
        # must start with StandInit 
        if state["moves_done"] == []:
            return ["StandInit"]

        #changing name to next_moves to avoid conflict with reserved python keyword "next"
        next_moves = []

        # adapting to new MOVES dict structure
        for move, info in MOVES.items():

            duration = info["duration"]
            requires = info["requires"]

            if (state["time"]+ duration) <= self.max_time and state["posture"]==requires:
                next_moves.append(move)
        return next_moves

    def result(self, state, action):
        '''
        The resulting state from executing the passed action to the passed state
        - time increases based on the move executed
        - mandatory_left drops the completed move from the begining 
        - incrementing the intermediate_count (if applied)
        '''
        #taking all info about the move called (action represents the move name)
        # again no logic changes, just adapting to new MOVES dict structure
        info = MOVES[action]

        result_state = state.copy()

        result_state["time"]+=info["duration"]

        #changing to always access self variables, so we don't change a global structure
        if action in result_state["mandatory_left"]:
            # importart fix, made a copy so we don't mutate the previous's state "mandatory_left" list
            # every state should have its own copy of the list for independence
            # so the algorithm can explore different branches correctly
            result_state["mandatory_left"] = result_state["mandatory_left"].copy()
            result_state["mandatory_left"].remove(action)
        elif action in self.INTERMEDIATE:
            result_state["intermediate_count"]+=1

        result_state["posture"] = info["produces"]
        result_state["moves_done"] = state["moves_done"] + [action]

        return result_state

    def goal_test(self, state):
        '''
        Check:
        - are all mandatory moves done (set empty)
        - at least 5 intermediate moves performed
        - the total time is less than or equal to 120 seconds
        '''
        return (
            #accessing self variable again for consistency and modularity
            state["time"] <= self.max_time and
            not state["mandatory_left"] and
            state["intermediate_count"] >= 5 and 
            state["moves_done"] and
            # final posture forced to Crouch
            state["moves_done"][-1] == "Crouch"
        )