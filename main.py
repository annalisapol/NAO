from search import iterative_deepening_search
from nao_problem import NaoProblem, from_state_to_dict
from constants import MOVES, MAX_TIME
from moves_helper import load_moves

import sys, time, os, yaml

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

pythonpath = config["pythonpath"]
ip = config["robot"]["ip"]
port = config["robot"]["port"]

if pythonpath not in sys.path:
    sys.path.append(pythonpath)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROBOT_POSITIONS = os.path.join(BASE_DIR, "RobotPositions")

moves = load_moves(ROBOT_POSITIONS)


class Move(object):
    def __init__(self, duration=None, preconditions=None, postconditions=None):
        self.duration = float(duration)
        self.preconditions = preconditions or {}
        self.postconditions = postconditions or {}


def build_intermediate_moves():
    
    # Build the dict of intermediate moves from constants.MOVES.
    # Convert requires/produces into 'standing' pre/postconditions.
   
    moves = {}
    for name, info in MOVES.items():
        if info.get('category') != 'intermediate':
            continue

        duration = info['duration']
        requires = info.get('requires')
        produces = info.get('produces')

        pre = {}
        post = {}

        if requires == 'standing':
            pre['standing'] = True
        elif requires == 'sitting':
            pre['standing'] = False

        if produces == 'standing':
            post['standing'] = True
        elif produces == 'sitting':
            post['standing'] = False

        moves[name] = Move(duration, pre, post)

    return moves


def posture_after(move_name):
    
    # Rough standing/non-standing output for mandatory moves,
    #based on constants.MOVES['produces'].
    
    info = MOVES.get(move_name, {})
    prod = info.get('produces')
    if prod == 'sitting':
        return False
    #everything else (standing, crouching, None) as standing=True
    return True


def posture_before(move_name):
    
    # Rough standing/non-standing requirement for mandatory moves,
    # based on constants.MOVES['requires'].
    
    info = MOVES.get(move_name, {})
    req = info.get('requires')
    if req == 'sitting':
        return False
    if req == 'standing':
        return True
    # no strict requirement -> None
    return None


def run_move(move_name):

    if move_name not in moves:
        print("[ERROR] Move not found:", move_name)
        return

    print("[RUNNING]", move_name)
    moves[move_name](ip, port)

def measure_move_time(move_name, ip, port):
    
    # Runs the real NAO move and measures how long it takes in seconds.
    
    if move_name not in moves:
        print("[ERROR] Move not found:", move_name)
        return 0.0

    print("[MEASURE]", move_name)
    start = time.time()
    try:
        moves[move_name](ip, port)
    except Exception as e:
        print("[ERROR during execution of %s] %s" % (move_name, e))
        return 0.0
    end = time.time()

    return end - start

def main():
    
    mandatory_order = [
        "StandInit",
        "WipeForehead",
        "Hello",
        "StandZero",
        "Sit",
        "Stand",
        "SitRelax",
        "Stand",
        "Crouch"
    ]

    #  (name, Move) list for mandatory moves
    mandatory_moves = []
    for name in mandatory_order:
        info = MOVES[name]
        mandatory_moves.append((name, Move(info['duration'])))

    # dictionary of intermediate moves
    intermediate_moves = build_intermediate_moves()

    # Compute total time of mandatory moves
    total_mand_time = sum(m[1].duration for m in mandatory_moves)
    if total_mand_time > MAX_TIME:
        print("ERROR: mandatory moves alone exceed MAX_TIME = %.2f" % MAX_TIME)
        print("Total mandatory time: %.2f" % total_mand_time)
        return

    # Remaining time available for intermediate moves
    segments = len(mandatory_moves) - 1  # number of segments between mandatories
    time_for_intermediates = MAX_TIME - total_mand_time

    # insert intermediates in segments where both sides are standing.and distribute time fairly.
    standing_segments = 0
    segment_is_standing = []
    for i in range(1, len(mandatory_moves)):
        start_name = mandatory_moves[i - 1][0]
        end_name = mandatory_moves[i][0]

        start_post = posture_after(start_name)
        end_pre = posture_before(end_name)

        if start_post is True and (end_pre is None or end_pre is True):
            segment_is_standing.append(True)
            standing_segments += 1
        else:
            segment_is_standing.append(False)

    if standing_segments > 0:
        per_segment_time = time_for_intermediates / float(standing_segments)
    else:
        per_segment_time = 0.0

    print("Planning choreography...")
    print("Total mandatory time: %.2f s, remaining for intermediates: %.2f s" %
          (total_mand_time, time_for_intermediates))

    full_choreo = ()
    total_intermediate_moves = 0

    # For each segment, plan local choreography between mandatory moves
    for idx in range(1, len(mandatory_moves)):
        start_name = mandatory_moves[idx - 1][0]
        end_name = mandatory_moves[idx][0]

        print(" Segment %d: %s -> %s" % (idx, start_name, end_name))

        if segment_is_standing[idx - 1]:
            required_moves = 2  # to be decided ..
            segment_time = per_segment_time
        else:
            required_moves = 0
            segment_time = 0.0

        if required_moves == 0:
           
            if idx == 1:
                full_choreo += (start_name,)
            full_choreo += (end_name,)
            print("  -> no intermediates (posture change segment or non-standing).")
            continue

        start_post_standing = posture_after(start_name)

        choreography = (start_name,)
        initial_state = (
            ('choreography', choreography),
            ('standing', start_post_standing),
            ('remaining_time', segment_time),
            ('moves_done', 0),
        )

        goal_state = (
            ('standing', True),
            ('moves_done', required_moves),
        )

        problem = NaoProblem(initial_state, goal_state, intermediate_moves)
        solution_node = iterative_deepening_search(problem)

        if solution_node is None:
            print("  -> No solution found for this segment, no intermediates.")
            if idx == 1:
                full_choreo += (start_name,)
            full_choreo += (end_name,)
            continue

        sol_dict = from_state_to_dict(solution_node.state)
        seg_choreo = sol_dict['choreography']  # tuple: (start_name, inter1, inter2, ...)

        # Append to global choreography (avoid duplicating the  first move)
        if idx == 1:
            full_choreo += seg_choreo
        else:
            full_choreo += seg_choreo[1:]  # skip repeating start_name

        total_intermediate_moves += sol_dict['moves_done']

        # Finally append the end mandatory for this segment if not already last
        if full_choreo[-1] != end_name:
            full_choreo += (end_name,)

        print("  -> segment choreography:", " -> ".join(seg_choreo))

    print("\nFinal choreography:")
    print(" -> ".join(full_choreo))

    # Compute total time of full choreography
    total_time = 0.0
    for move_name in full_choreo:
        total_time += MOVES[move_name]['duration']

    print("\nTotal time: %.2f s (MAX_TIME = %.2f)" % (total_time, MAX_TIME))
    print("Total intermediate moves used:", total_intermediate_moves)

    print("\n REAL EXECUTION TIMING")

    real_total = 0.0
    real_times = {}

    for move_name in full_choreo:
        dt = measure_move_time(move_name, ip, port)
        real_times[move_name] = dt
        real_total += dt
        print("  %s : %.2f s" % (move_name, dt))

    print("\nREAL total execution time: %.2f s" % real_total)



if __name__ == "__main__":
    main()
