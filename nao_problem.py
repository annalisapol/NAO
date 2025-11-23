import random
from search import Problem


def from_state_to_dict(state):
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
        Problem.__init__(self, initial, goal)
        self.available_moves = moves

    def is_move_applicable(self, state, move_name, move):
      
        state_dict = from_state_to_dict(state)
        choreo = state_dict['choreography']
        last_move = choreo[-1]
        remaining_time = state_dict['remaining_time']
        standing = state_dict['standing']

        if remaining_time < move.duration:
            return False

        # standing preconditions
        if 'standing' in move.preconditions:
            if standing != move.preconditions['standing']:
                return False

        #avoid repeating same move twice in a row
        if move_name == last_move:
            return False

        return True

    def actions(self, state):
    
        actions = []
        state_dict = from_state_to_dict(state)
        choreo = state_dict['choreography']

        for move_name, move in self.available_moves.items():

            if choreo.count(move_name) >= 2:
                continue

            if self.is_move_applicable(state, move_name, move):
                actions.append(move_name)

        random.shuffle(actions)
        return actions
        

    def result(self, state, action):
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
        state_dict = from_state_to_dict(state)
        goal_dict = from_state_to_dict(self.goal)

        moves_done_constraint = (state_dict['moves_done'] >= goal_dict['moves_done'])

        goal_standing = goal_dict.get('standing', None)
        if goal_standing is None:
            return moves_done_constraint

        standing_constraint = (state_dict['standing'] == goal_standing)
        return moves_done_constraint and standing_constraint
