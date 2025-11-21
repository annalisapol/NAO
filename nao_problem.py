"""
NAO segment-planning problem

This problem is used ONLY for:
- planning intermediate moves between two mandatory moves
- given:
    - current choreography (tuple of move names)
    - current standing (True/False)
    - remaining_time for this segment
    - moves_done (int, number of intermediates in this segment)
"""

import random
from search import Problem


def from_state_to_dict(state):
    """
    Converts a state (tuple of tuples) into a dict.
    Example state:
      (('choreography', ('StandInit', 'Move1')),
       ('standing', True),
       ('remaining_time', 10.0),
       ('moves_done', 2))
    """
    params_dict = {}
    for t in state:
        if not t:
            continue
        key = t[0]
        if len(t) == 2:
            value = t[1]
        elif len(t) > 2:
            value = t[1:]
        else:
            continue
        params_dict[key] = value
    return params_dict


class NaoProblem(Problem):

    def __init__(self, initial, goal, moves):
        """
        initial: state (tuple of tuples)
        goal   : goal state (tuple of tuples), typically:
                 (('standing', True/False or None),
                  ('moves_done', k))
        moves  : dict name -> Move(duration, preconditions, postconditions)
        """
        Problem.__init__(self, initial, goal)
        self.available_moves = moves

    def is_move_applicable(self, state, move_name, move):
        """
        Check whether 'move_name' can be executed in 'state'.
        Criteria (simplified from the other group):
          1) enough remaining_time
          2) standing preconditions satisfied (if any)
          3) avoid repeating the same move as the last one
        """
        state_dict = from_state_to_dict(state)
        choreo = state_dict['choreography']
        last_move = choreo[-1]
        remaining_time = state_dict['remaining_time']
        standing = state_dict['standing']

        # 1: time constraint
        if remaining_time < move.duration:
            return False

        # 2: standing preconditions
        if 'standing' in move.preconditions:
            if standing != move.preconditions['standing']:
                return False

        # 3: avoid repeating same move twice in a row
        if move_name == last_move:
            return False

        return True

    def actions(self, state):
        """
        Returns the list of possible move names from 'available_moves'
        that satisfy applicability.
        """
        actions = []
        for move_name, move in self.available_moves.items():
            if self.is_move_applicable(state, move_name, move):
                actions.append(move_name)
        # Randomize to get some variety
        random.shuffle(actions)
        return actions

    def result(self, state, action):
        """
        Apply move 'action' to 'state', return new state.
        Updates:
          - choreography: append action
          - standing: updated via move.postconditions if present
          - remaining_time: minus move.duration
          - moves_done: +1
        """
        move = self.available_moves[action]
        state_dict = from_state_to_dict(state)

        old_standing = state_dict['standing']
        remaining_time = state_dict['remaining_time']
        moves_done = state_dict['moves_done']
        choreo = state_dict['choreography']

        # standing change
        if 'standing' in move.postconditions:
            new_standing = move.postconditions['standing']
        else:
            new_standing = old_standing

        new_state = (
            ('choreography', tuple(list(choreo) + [action])),
            ('standing', new_standing),
            ('remaining_time', remaining_time - move.duration),
            ('moves_done', moves_done + 1),
        )
        return new_state

    def goal_test(self, state):
        """
        A state is goal if:
          - moves_done >= goal['moves_done']
          - if goal specifies 'standing' (not None), then standing matches
        """
        state_dict = from_state_to_dict(state)
        goal_dict = from_state_to_dict(self.goal)

        moves_done_constraint = (state_dict['moves_done'] >= goal_dict['moves_done'])

        goal_standing = goal_dict.get('standing', None)
        if goal_standing is None:
            return moves_done_constraint

        standing_constraint = (state_dict['standing'] == goal_standing)
        return moves_done_constraint and standing_constraint
