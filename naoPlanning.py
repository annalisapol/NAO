# -*- coding: utf-8 -*-
import random
from search import Problem
from constants_adapter import intermediatePos, mandatoryPos, initialPos, goalPos
from constants import MOVES

# Build a mandatory-moves set
MANDATORY_SET = frozenset([
    name for name, info in MOVES.items()
    if info["category"] == "mandatory"
])

class NaoProblem(Problem):
    """
    NEW planner:
    - State is a dict (pose, isStanding, time_used, done_mandatory)
    - All mandatory moves must be done at least once
    - End with Crouch
    """

    def __init__(self, initial, goal):
        Problem.__init__(self, initial, goal)
        self.max_time = 120.0
        self.moves = {name: MOVES[name] for name in MOVES}

    # --------------------------------------------
    # ACTIONS
    # --------------------------------------------
    def actions(self, state):
        available = []

        for name, move in self.moves.items():
            # cannot repeat exact same pose consecutively
            if name == state["pose"]:
                continue

            # check precondition: standing/sitting
            req = move["requires"]
            if req == "standing" and not state["isStanding"]:
                continue
            if req == "sitting" and state["isStanding"]:
                continue
            # "requires": None → allowed

            # check time limit
            if state["time_used"] + move["duration"] > self.max_time:
                continue

            available.append(name)

        random.shuffle(available)
        return available

    # --------------------------------------------
    # RESULT
    # --------------------------------------------
    def result(self, state, action):
        move = self.moves[action]

        new_state = {
            "pose": action,
            "isStanding": True if move["produces"] == "standing" else False,
            "time_used": state["time_used"] + move["duration"],
            "done_mandatory": state["done_mandatory"]
        }

        # update mandatory set
        if action in MANDATORY_SET:
            new_state["done_mandatory"] = state["done_mandatory"] | frozenset([action])

        return new_state

    # --------------------------------------------
    # GOAL TEST
    # --------------------------------------------
    def goal_test(self, state):
        # must be in final pose
        if state["pose"] != "Crouch":
            return False

        # must have completed ALL mandatory moves
        if not MANDATORY_SET.issubset(state["done_mandatory"]):
            return False

        # must satisfy preconditions for final
        # crouch requires standing
        if state["isStanding"] is False:
            return False

        # time already checked in transitions, but safe:
        if state["time_used"] > self.max_time:
            return False

        return True

    # --------------------------------------------
    # HEURISTIC for A*
    # --------------------------------------------
    def h(self, node):
        state = node.state

        # sum minimum durations of remaining mandatory moves
        remaining = MANDATORY_SET - state["done_mandatory"]

        h_time = sum(MOVES[m]["duration"] for m in remaining)

        # need to add cost for final Crouch
        h_time += MOVES["Crouch"]["duration"]

        return h_time
