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
        return (
            self.mandatory_left == other.mandatory_left and
            self.intermediate_count == other.intermediate_count and
            self.posture == other.posture
        )

    def __hash__(self):
        return hash((
            self.mandatory_left,
            self.intermediate_count,
            self.posture
        ))


class NAOProblem(Problem):
    def __init__(self, initial="StandInit", goal="Crouch"):
        
        self.MANDATORY = set(get_mandatory_moves())
        self.INTERMEDIATE = set(get_intermediate_moves())
       
        initial_posture = MOVES["StandInit"]["produces"]
       
        initial_state = NAOState(
            time=0,
            mandatory_left=self.MANDATORY.copy(),
            intermediate_count=0,
            posture=initial_posture,
            moves_done=[],
            last_move=None,
        )

        Problem.__init__(self, initial_state, goal)
        self.max_time = MAX_TIME

    def actions(self, state):

        print("\n--- STATE ---")
        print("time:", state.time)
        print("posture:", state.posture)
        print("mandatory_left:", state.mandatory_left)
        print("intermediate_count:", state.intermediate_count)
        print("last_move:", state.last_move)


        available = []

        for move, info in MOVES.items():
            
            if len(state.moves_done) == 0 and move != "StandInit":
                continue

            if state.time + info["duration"] > self.max_time:
                continue

            if state.posture != info["requires"]:
                continue

            available.append(move)

        return available

    def result(self, state, action):
        info = MOVES[action]
        
        new_mandatory = set(state.mandatory_left)
        if action in new_mandatory:
            new_mandatory.remove(action)

        new_intermediate = state.intermediate_count
        if action in self.INTERMEDIATE:
            new_intermediate += 1

        return NAOState(
            time = state.time + info["duration"],
            mandatory_left = new_mandatory,
            intermediate_count = new_intermediate,
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
