from search import Problem
from constants import MOVES, MAX_TIME


class NAOState(object):
    """
    Minimal state representation:
    Search state = posture + mandatory_left
    NOTE: intermediate_count and time are NOT part of the equality test
    to allow pruning and avoid infinite loops.
    """

    def __init__(self, posture, mandatory_left, inter_count, time):
        self.posture = posture
        self.mandatory_left = frozenset(mandatory_left)
        self.inter_count = inter_count
        self.time = time

    def __eq__(self, other):
        return (
            isinstance(other, NAOState) and
            self.posture == other.posture and
            self.mandatory_left == other.mandatory_left
        )

    def __hash__(self):
        return hash((self.posture, self.mandatory_left))

    def __repr__(self):
        return "<State posture=%s mand_left=%s inter=%d time=%.2f>" % (
            self.posture, list(self.mandatory_left),
            self.inter_count, self.time
        )


class NAOProblem(Problem):

    def __init__(self):
        # sets
        self.mandatory_moves = {m for m,v in MOVES.items() if v["category"] == "mandatory"}
        self.intermediate_moves = {m for m,v in MOVES.items() if v["category"] == "intermediate"}

        # StandInit posture
        initial_posture = MOVES["StandInit"]["produces"]

        initial_state = NAOState(
            posture = initial_posture,
            mandatory_left = self.mandatory_moves.copy(),
            inter_count = 0,
            time = 0
        )

        # Python2: explicit constructor call
        Problem.__init__(self, initial_state)

        self.max_time = MAX_TIME


    # ------------------------------------------------------------
    def actions(self, state):

        # First move is ALWAYS StandInit
        if state.time == 0:
            return ["StandInit"]

        possible = []

        for move, info in MOVES.items():

            # Always allow Crouch ONLY at the end
            if move == "Crouch":
                if len(state.mandatory_left) == 0 and state.inter_count >= 5:
                    # OK
                    pass
                else:
                    continue

            # Respect posture
            if state.posture != info["requires"]:
                continue

            # Time check
            if state.time + info["duration"] > self.max_time:
                continue

            possible.append(move)

        return possible


    # ------------------------------------------------------------
    def result(self, state, action):

        info = MOVES[action]

        # update mandatory
        new_mand = set(state.mandatory_left)
        if action in new_mand:
            new_mand.remove(action)

        # intermediate counter
        new_inter = state.inter_count
        if action in self.intermediate_moves:
            new_inter += 1

        return NAOState(
            posture = info["produces"],
            mandatory_left = new_mand,
            inter_count = new_inter, 
            time = state.time + info["duration"]
        )


    # ------------------------------------------------------------
    def goal_test(self, state):
        return (
            len(state.mandatory_left) == 0 and
            state.inter_count >= 5 and
            state.time <= self.max_time and
            # Must end with final action Crouch:
            # state.action is not stored; instead check posture
            state.posture == MOVES["Crouch"]["crouching"]
        )
