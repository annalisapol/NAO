# This file defines the NAOProblem class used for search-based planning.
# It encodes the robot's possible moves, constraints, and how states
# transition during the choreography planning 
from search import Problem
from constants import MOVES, MAX_TIME
from moves_helper import (
    get_mandatory_moves,
    get_intermediate_moves)

    
class NAOState(object):
    def __init__(self, time, mandatory_left, intermediate_count, posture, moves_done, last_move):
        self.time = time
        self.mandatory_left = frozenset(mandatory_left)
        self.intermediate_count = intermediate_count
        self.posture = posture
        self.moves_done = tuple(moves_done)
        self.last_move = last_move

    def __eq__(self, other):
        return isinstance(other, NAOState) and (
            self.time == other.time and
            self.mandatory_left == other.mandatory_left and
            self.intermediate_count == other.intermediate_count and
            self.posture == other.posture and
            self.moves_done == other.moves_done and
            self.last_move == other.last_move
        )

    def __hash__(self):
        return hash((
            self.time,
            self.mandatory_left,
            self.intermediate_count,
            self.posture,
            self.moves_done,
            self.last_move
        ))

class NAOProblem(Problem):
    def __init__(self, initial="StandInit", goal="Crouch"):
        
        self.MANDATORY = set(get_mandatory_moves())
        self.INTERMEDIATE = set(get_intermediate_moves())
       
        # INITIAL POSTURE must match MOVES["StandInit"]["produces"]
        initial_posture = MOVES["StandInit"]["produces"]
       
        # The initial state: no time, all mandatory left, no moves done
        initial_state = NAOState(
            time=0,
            mandatory_left=self.MANDATORY.copy(),
            intermediate_count=0,
            posture=initial_posture,
            moves_done=[],
            last_move=None,
        )

        # Call Problem constructor with a HASHABLE state
        Problem.__init__(self, initial_state, goal)

        self.max_time = MAX_TIME

    def actions(self, state):

        # First move must be StandInit
        """ if len(state.moves_done) == 0:
            return ["StandInit"]
        """
        available = []

        for move, info in MOVES.items():
            
            if len(state.moves_done) == 0 and move != "StandInit":
                continue

            # Cannot exceed 120s
            if state.time + info["duration"] > self.max_time:
                continue

            # Check posture requirement
            if state.posture != info["requires"]:
                continue

            # Optional: incompatibility check (later)
            # if move in self.incompatibilities.get(state.last_move, []):
            #     continue

            available.append(move)

        return available

    def result(self, state, action):
        info = MOVES[action]
        
        # Compute new mandatory set
        new_mandatory= set(state.mandatory_left)

        if action in new_mandatory:
            new_mandatory.remove(action)

        # Compute intermediate count
        new_intermediate = state.intermediate_count
        if action in self.INTERMEDIATE:
            new_intermediate += 1

        # Build new state object
        return NAOState(
            time = state.time + info["duration"],
            mandatory_left = new_mandatory,
            intermediate_count = new_intermediate, #use a list of the used intermediate moves indtead of the counter 
            posture = info["produces"],
            moves_done = list(state.moves_done) + [action],
            last_move = action
        )

    def goal_test(self, state):
        return (
            state.time <= self.max_time and
            len(state.mandatory_left) == 0 and
            state.intermediate_count >= 5 and
            len(state.moves_done) > 0 and
            state.moves_done[-1] == self.goal
        )
