# This file defines the NAOProblem class used for search-based planning.
# It encodes the robot's possible moves, constraints, and how states
# transition during the choreography planning 
from search import Problem
from constants import *
from utils import distance

class NAOProblem(Problem):
    def __init__(self, state, move_durations, incompatibilities, max_time=MAX_TIME):
        '''
        Initialize the planning problem with:
        - Initial state
        - Goal conditions
        - Durations of each move
        - Incompatibility constraints
        - Maximum allowed time (2 min = 120s)
        '''
        self.state={
            "time": 0,
            "mandatory_left": set(MANDATORY),
            "intermediate_count":0
            "posture": "None"
            # changing this to None because "Stand" still needs to be computed, since time is at 0
            # initial posture is undefined
        }
        
        super().__init___(self.state,None)
        self.max_time = max_time,
        self.move_durations = move_durations #should be a dict mapping each move to its duration in seconds, maybe at the fastest speed
        self.incompatibilities = incompatibilities #to be defined, should be a dict mapping each move to the list of incompatible moves

    def action(self, state):
        '''
        Return all possible moves that the robot can execute from the current states
        This applies filters for:
        - Time limit 
        - Incompatibilities with previous move
        - Posture requirements (standing/sitting)
        '''
        next = []
        for move, conditions in MOVE_CONDITIONS.items():
            if (state["time"]+ MOVE_TIME[move]) <= 120 and state["posture"]==conditions["requires"]:
                next.append(move)
        return next
    def result(self, state, action):
        '''
        The resulting state from executing the passed action to the passed state
        - time increases based on the move executed
        - mandatory_left drops the completed move from the begining 
        - incrementing the intermediate_count (if applied)
        '''
        result_state = state.copy()
        result_state["time"]+=MOVE_TIME[action]
        if action in MANDATORY:
            result_state["mandatory_left"].remove(action)
        elif action in INTERMEDIATE:
            result_state["intermediate_count"]+=1
        result_state["posture"]=MOVE_CONDITIONS[action]["produces"]
        return result_state

    def goal_test(self, state):
        '''
        Check:
        - are all mandatory moves done (set empty)
        - at least 5 intermediate moves performed
        - the total time is less than or equal to 120 seconds
        '''
        return (
            state["time"] <= 120 and
            not state["mandatory_left"] and
            state["intermediate_count"] >= 5
        )