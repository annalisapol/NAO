# -*- coding: utf-8 -*-
from search import iterative_deepening_search
from nao_problem import NaoProblem, from_state_to_dict
from constants import MOVES, MAX_TIME
from moves_helper import load_moves
from naoqi import ALProxy
import sys, time, os, yaml

# ----- LOAD CONFIG -----
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

pythonpath = config["pythonpath"]
ip = config["robot"]["ip"]
port = config["robot"]["port"]

# add pythonpath for robot positions
if pythonpath not in sys.path:
    sys.path.append(pythonpath)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROBOT_POSITIONS = os.path.join(BASE_DIR, "RobotPositions")

# load all move scripts
moves = load_moves(ROBOT_POSITIONS)


# ----- HELPER CLASSES -----
class Move(object):
    def __init__(self, duration=None, preconditions=None, postconditions=None):
        self.duration = float(duration)
        self.preconditions = preconditions or {}
        self.postconditions = postconditions or {}


# Build intermediate-only moves + their standing/sitting constraints
def build_intermediate_moves():
    moves_dict = {}
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

        moves_dict[name] = Move(duration, pre, post)

    return moves_dict


# Standing or sitting after a mandatory move?
def posture_after(move_name):
    info = MOVES.get(move_name, {})
    prod = info.get('produces')
    if prod == 'sitting':
        return False
    return True


# Standing or sitting required before the move?
def posture_before(move_name):
    info = MOVES.get(move_name, {})
    req = info.get('requires')
    if req == 'sitting':
        return False
    if req == 'standing':
        return True
    return None


# Execute a move with the loaded NAOqi functions
def run_move(move_name):
    if move_name not in moves:
        print("[ERROR] Move not found:", move_name)
        return
    print("[RUNNING]", move_name)
    moves[move_name](ip, port)


# Measure real execution time for each move
def measure_move_time(move_name, ip, port):
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


# ----- MAIN PIPELINE -----
def main():

    # Create the NAO audio player proxy.
    audio = ALProxy("ALAudioPlayer", ip, port)

    # Path to the selected song (converted to WAV).
    # This will be played asynchronously during dance moves.
    song_path = os.path.join(BASE_DIR, "music", "levitating.wav")

    # Mandatory move sequence (fixed order)
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

    # Prepare mandatory moves with durations
    mandatory_moves = []
    for name in mandatory_order:
        info = MOVES[name]
        mandatory_moves.append((name, Move(info['duration'])))

    # Load intermediate moves
    intermediate_moves = build_intermediate_moves()

    # Compute total mandatory time
    total_mand_time = sum(m[1].duration for m in mandatory_moves)
    if total_mand_time > MAX_TIME:
        print("ERROR: mandatory moves alone exceed MAX_TIME = %.2f" % MAX_TIME)
        return

    # Time budget for intermediates
    segments = len(mandatory_moves) - 1
    time_for_intermediates = MAX_TIME - total_mand_time

    # Identify where intermediate moves are allowed (only standing→standing)
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

    per_segment_time = (time_for_intermediates / float(standing_segments)) if standing_segments > 0 else 0.0

    print("Planning choreography...")
    print("Total mandatory time: %.2f s, remaining for intermediates: %.2f s"
          % (total_mand_time, time_for_intermediates))

    full_choreo = ()
    total_intermediate_moves = 0

    # ----- PLAN FOR EVERY SEGMENT -----
    for idx in range(1, len(mandatory_moves)):
        start_name = mandatory_moves[idx - 1][0]
        end_name = mandatory_moves[idx][0]

        print(" Segment %d: %s -> %s" % (idx, start_name, end_name))

        required_moves = 2 if segment_is_standing[idx - 1] else 0
        segment_time = per_segment_time if required_moves else 0.0

        if required_moves == 0:
            if idx == 1:
                full_choreo += (start_name,)
            full_choreo += (end_name,)
            print("  -> no intermediates (posture change or sitting).")
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

        # Run the search algorithm
        problem = NaoProblem(initial_state, goal_state, intermediate_moves)
        solution_node = iterative_deepening_search(problem)

        if solution_node is None:
            print("  -> No solution for this segment.")
            if idx == 1:
                full_choreo += (start_name,)
            full_choreo += (end_name,)
            continue

        sol_dict = from_state_to_dict(solution_node.state)
        seg_choreo = sol_dict['choreography']

        if idx == 1:
            full_choreo += seg_choreo
        else:
            full_choreo += seg_choreo[1:]  # skip repeating the start move

        total_intermediate_moves += sol_dict['moves_done']

        if full_choreo[-1] != end_name:
            full_choreo += (end_name,)

        print("  -> segment choreography:", " -> ".join(seg_choreo))

    # ----- FINAL CHOREOGRAPHY -----
    print("\nFinal choreography:")
    print(" -> ".join(full_choreo))

    total_time = sum(MOVES[m]['duration'] for m in full_choreo)
    print("\nTotal time: %.2f s (MAX_TIME = %.2f)" % (total_time, MAX_TIME))
    print("Total intermediate moves used:", total_intermediate_moves)

    print("\n REAL EXECUTION TIMING")

    real_total = 0.0
    real_times = {}

    # ----- START MUSIC ASYNCHRONOUSLY -----
    print("\nStarting music...")
    music_task_id = None

    try:
        # async playback → returns a task ID we can stop later
        music_task_id = audio.post.playFile(song_path)
        print("[INFO] Music started, task id:", music_task_id)
    except Exception as e:
        print("[ERROR] Could not play music:", e)


    # ----- EXECUTE MOVES -----
    for move_name in full_choreo:
        dt = measure_move_time(move_name, ip, port)
        real_times[move_name] = dt
        real_total += dt
        print("  %s : %.2f s" % (move_name, dt))

    print("\nREAL total execution time: %.2f s" % real_total)

    # ----- STOP MUSIC -----
    print("Stopping music...")
    try:
        if music_task_id is not None:
            audio.stop(music_task_id)   # stop only that song
        else:
            audio.stopAll()
    except:
        pass



if __name__ == "__main__":
    main()
