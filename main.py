# -*- coding: utf-8 -*-
from search import iterative_deepening_search
from nao_problem import NaoProblem, from_state_to_dict
from constants import MOVES, MAX_TIME
from moves_helper import load_moves
from naoqi import ALProxy
import sys, time, os, yaml


# ---------------- LOAD CONFIG ----------------
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


# ---------------- MOVE CLASS ----------------
class Move(object):
    def __init__(self, duration=None, preconditions=None, postconditions=None):
        self.duration = float(duration)
        self.preconditions = preconditions or {}
        self.postconditions = postconditions or {}


# ---------------- BUILD INTERMEDIATE MOVES ----------------
def build_intermediate_moves():
    m = {}
    for name, info in MOVES.items():
        if info.get("category") != "intermediate":
            continue

        dur = info["duration"] + 0.9  # consistent with planning timing
        req = info.get("requires")
        prod = info.get("produces")

        pre = {}
        post = {}

        if req == "standing":
            pre["standing"] = True
        elif req == "sitting":
            pre["standing"] = False

        if prod == "standing":
            post["standing"] = True
        elif prod == "sitting":
            post["standing"] = False

        m[name] = Move(dur, pre, post)
    return m


# ---------------- POSTURE FUNCTIONS ----------------
def posture_after(move_name):
    """Return True = standing, False = sitting"""
    prod = MOVES.get(move_name, {}).get("produces")
    return False if prod == "sitting" else True


def posture_before(move_name):
    req = MOVES.get(move_name, {}).get("requires")
    if req == "sitting":
        return False
    if req == "standing":
        return True
    return None


# ---------------- EXECUTION HELPERS ----------------
def stabilize():
    """Stabilize robot before/after each move."""
    try:
        motionProxy.wbEnable(False)
        motionProxy.setStiffnesses("Body", 1.0)
        postureProxy.goToPosture("StandInit", 0.7)
        time.sleep(0.3)
    except Exception as e:
        print("[WARN] Stabilization issue:", e)


def measure_move_time(move_name, ip, port):
    if move_name not in moves:
        print("[ERROR] Move not found:", move_name)
        return 0.0

    stabilize()
    print("[MEASURE]", move_name)
    t0 = time.time()
    try:
        moves[move_name](ip, port)
    except Exception as e:
        print("[ERROR during %s] %s" % (move_name, e))
        return 0.0
    t1 = time.time()
    stabilize()
    return t1 - t0


# ---------------- MAIN ----------------
def main():
    global postureProxy, motionProxy
    postureProxy = ALProxy("ALRobotPosture", ip, port)
    motionProxy = ALProxy("ALMotion", ip, port)
    audio = ALProxy("ALAudioPlayer", ip, port)

    song_path = os.path.join(BASE_DIR, "music", "levitating.wav")

    # TEAMMATE'S FINAL MANDATORY ORDER
    mandatory_order = [
        "StandInit",
        "WipeForehead",
        "Hello",
        "StandZero",
        "Sit",
        "VOnEyes",
        "SitRelax",
        "Stand",
        "Crouch"
    ]

    mandatory_moves = [(name, Move(MOVES[name]["duration"] + 0.9))
                       for name in mandatory_order]

    intermediate_moves = build_intermediate_moves()

    total_mand = sum(m[1].duration for m in mandatory_moves)
    if total_mand > MAX_TIME:
        print("ERROR: mandatory exceed MAX_TIME", total_mand)
        return

    time_for_inter = MAX_TIME - total_mand
    segments = len(mandatory_moves) - 1

    # Standing segments detection
    standing_segments = 0
    seg_ok = []
    for i in range(1, len(mandatory_moves)):
        start = mandatory_moves[i-1][0]
        end = mandatory_moves[i][0]

        start_post = posture_after(start)
        end_pre = posture_before(end)

        ok = start_post is True and (end_pre in [True, None])
        seg_ok.append(ok)
        if ok:
            standing_segments += 1

    per_segment_time = (time_for_inter / standing_segments) if standing_segments else 0

    print("Planning choreography...")
    print("Mandatory time:", total_mand, "Remaining:", time_for_inter)

    full = ()
    used_intermediates = set()
    total_inter = 0

    # ------------ PLAN EACH SEGMENT ------------
    for idx in range(1, len(mandatory_moves)):
        start = mandatory_moves[idx-1][0]
        end = mandatory_moves[idx][0]

        print("\nSegment %d: %s -> %s" % (idx, start, end))

        # SPECIAL CASE: Stand → SitRelax MUST have no intermediates
        if end == "SitRelax":
            print("  -> Forcing no intermediates for SitRelax transition.")
            if idx == 1:
                full += (start,)
            full += (end,)
            continue

        required = 1 if seg_ok[idx-1] else 0   # OPTION E: exactly 1
        seg_time = per_segment_time if required else 0

        if required == 0:
            if idx == 1:
                full += (start,)
            full += (end,)
            print("  -> Non-standing segment: no intermediates.")
            continue

        # Build search problem
        start_standing = posture_after(start)
        initial = (
            ('choreography', (start,)),
            ('standing', start_standing),
            ('remaining_time', seg_time),
            ('moves_done', 0),
        )
        goal = (('standing', True), ('moves_done', required))

        # Encourage non-used moves first
        candidate_moves = {n: m for n, m in intermediate_moves.items()
                           if n not in used_intermediates}
        if len(candidate_moves) < required:
            candidate_moves = intermediate_moves

        print("  -> Using intermediate pool:", list(candidate_moves.keys())[:5], "...")

        problem = NaoProblem(initial, goal, candidate_moves)
        sol = iterative_deepening_search(problem)

        if sol is None:
            print("  -> No solution found.")
            if idx == 1:
                full += (start,)
            full += (end,)
            continue

        sol_dict = from_state_to_dict(sol.state)
        choreo = sol_dict['choreography']

        # update global
        if idx == 1:
            full += choreo
        else:
            full += choreo[1:]

        # track used
        for m in choreo:
            if m in intermediate_moves:
                used_intermediates.add(m)

        total_inter += sol_dict['moves_done']

        if full[-1] != end:
            full += (end,)

        print("  -> segment:", " -> ".join(choreo))


    # ---------- FINAL CHOREO ----------
    print("\nFINAL CHOREOGRAPHY:")
    print(" -> ".join(full))

    planned_total = sum(MOVES[m]["duration"] + 0.9 for m in full)
    print("\nPlanned total:", planned_total, "MAX=", MAX_TIME)
    print("Intermediate used:", total_inter)

    # ---------- START MUSIC ASYNC ----------
    print("\nStarting music...")
    try:
        music_id = audio.post.playFile(song_path)
        print("[OK] Music playing with task ID:", music_id)
    except Exception as e:
        print("[ERROR] Could not play music:", e)
        music_id = None

    # ---------- EXECUTE SEQUENCE ----------
    real_total = 0
    for m in full:
        dt = measure_move_time(m, ip, port)
        real_total += dt
        print("  %s : %.2f s" % (m, dt))

    print("\nREAL total time:", real_total)

    # ---------- STOP MUSIC ----------
    print("Stopping music...")
    try:
        if music_id:
            audio.stop(music_id)
        else:
            audio.stopAll()
    except:
        pass


if __name__ == "__main__":
    main()
