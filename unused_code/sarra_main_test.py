#this code worked and made the execution tame so much lesser than 120s but it was way too less
'''
EXAMPLE OF THE RESUTLS
nao@nao-VirtualBox:~/NAO$ python2 main.py
[I] 6670 qimessaging.session: Session listener created on tcp://0.0.0.0:0
[I] 6670 qimessaging.transportserver: TransportServer will listen on: tcp://10.0.2.15:39771
[I] 6670 qimessaging.transportserver: TransportServer will listen on: tcp://127.0.0.1:39771
Planning choreography...
Total mandatory time: 55.29 s, remaining: 64.71 s
 Segment 1: StandInit -> WipeForehead
('  -> segment choreography:', 'StandInit -> ArmDanceSX')
 Segment 2: WipeForehead -> Hello
('  -> segment choreography:', 'WipeForehead -> ArmDanceSX')
 Segment 3: Hello -> StandZero
('  -> segment choreography:', 'Hello -> DiagonalLeft')
 Segment 4: StandZero -> Sit
('  -> segment choreography:', 'StandZero -> Sprinkler2')
 Segment 5: Sit -> Stand
  -> no intermediates.
 Segment 6: Stand -> SitRelax
('  -> segment choreography:', 'Stand -> VOnEyes')
 Segment 7: SitRelax -> Stand
  -> no intermediates.
 Segment 8: Stand -> Crouch
('  -> segment choreography:', 'Stand -> DiagonalLeft')

Final choreography:
StandInit -> ArmDanceSX -> WipeForehead -> ArmDanceSX -> Hello -> DiagonalLeft -> StandZero -> Sprinkler2 -> Sit -> Stand -> VOnEyes -> SitRelax -> Stand -> DiagonalLeft -> Crouch

Total time: 94.85 s (MAX = 120.00)
('Total intermediate moves used:', 6)

 REAL EXECUTION TIMING
('[MEASURE]', 'StandInit')
  StandInit : 0.22 s
('[MEASURE]', 'ArmDanceSX')
  ArmDanceSX : 5.01 s
('[MEASURE]', 'WipeForehead')
  WipeForehead : 6.25 s
('[MEASURE]', 'ArmDanceSX')
  ArmDanceSX : 5.04 s
('[MEASURE]', 'Hello')
  Hello : 5.85 s
('[MEASURE]', 'DiagonalLeft')
  DiagonalLeft : 2.48 s
('[MEASURE]', 'StandZero')
  StandZero : 0.94 s
('[MEASURE]', 'Sprinkler2')
  Sprinkler2 : 5.02 s
('[MEASURE]', 'Sit')
  Sit : 8.45 s
('[MEASURE]', 'Stand')
  Stand : 0.74 s
('[MEASURE]', 'VOnEyes')
  VOnEyes : 6.26 s
('[MEASURE]', 'SitRelax')
  SitRelax : 11.12 s
('[MEASURE]', 'Stand')
  Stand : 0.74 s
('[MEASURE]', 'DiagonalLeft')
  DiagonalLeft : 2.48 s
('[MEASURE]', 'Crouch')
  Crouch : 2.04 s

REAL total execution time: 62.64 s
nao@nao-VirtualBox:~/NAO$ python2 main.py
[I] 7026 qimessaging.session: Session listener created on tcp://0.0.0.0:0
[I] 7026 qimessaging.transportserver: TransportServer will listen on: tcp://10.0.2.15:33957
[I] 7026 qimessaging.transportserver: TransportServer will listen on: tcp://127.0.0.1:33957
Planning choreography...
Total mandatory time: 55.29 s, remaining: 64.71 s
 Segment 1: StandInit -> WipeForehead
('  -> segment choreography:', 'StandInit -> RotationHandgunObject')
 Segment 2: WipeForehead -> Hello
('  -> segment choreography:', 'WipeForehead -> ArmDanceDX')
 Segment 3: Hello -> StandZero
('  -> segment choreography:', 'Hello -> Disco')
 Segment 4: StandZero -> Sit
('  -> segment choreography:', 'StandZero -> VOnEyes')
 Segment 5: Sit -> Stand
  -> no intermediates.
 Segment 6: Stand -> SitRelax
('  -> segment choreography:', 'Stand -> RotationHandgunObject')
 Segment 7: SitRelax -> Stand
  -> no intermediates.
 Segment 8: Stand -> Crouch
('  -> segment choreography:', 'Stand -> MoveForward')

Final choreography:
StandInit -> RotationHandgunObject -> WipeForehead -> ArmDanceDX -> Hello -> Disco -> StandZero -> VOnEyes -> Sit -> Stand -> RotationHandgunObject -> SitRelax -> Stand -> MoveForward -> Crouch

Total time: 96.39 s (MAX = 120.00)
('Total intermediate moves used:', 6)

 REAL EXECUTION TIMING
('[MEASURE]', 'StandInit')
  StandInit : 0.22 s
('[MEASURE]', 'RotationHandgunObject')
  RotationHandgunObject : 4.06 s
('[MEASURE]', 'WipeForehead')
  WipeForehead : 6.26 s
('[MEASURE]', 'ArmDanceDX')
  ArmDanceDX : 5.02 s
('[MEASURE]', 'Hello')
  Hello : 5.86 s
('[MEASURE]', 'Disco')
  Disco : 5.02 s
('[MEASURE]', 'StandZero')
  StandZero : 0.94 s
('[MEASURE]', 'VOnEyes')
  VOnEyes : 6.25 s
('[MEASURE]', 'Sit')
  Sit : 8.46 s
('[MEASURE]', 'Stand')
  Stand : 0.74 s
('[MEASURE]', 'RotationHandgunObject')
  RotationHandgunObject : 4.06 s
('[MEASURE]', 'SitRelax')
  SitRelax : 9.00 s
('[MEASURE]', 'Stand')
  Stand : 0.74 s
('[MEASURE]', 'MoveForward')
  MoveForward : 2.90 s
('[MEASURE]', 'Crouch')
  Crouch : 2.04 s

REAL total execution time: 61.57 s
'''
'''
from search import iterative_deepening_search
from nao_problem import NaoProblem, from_state_to_dict
from constants import MOVES, MAX_TIME
from moves_helper import load_moves
from naoqi import ALProxy

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
    moves_dict = {}
    for name, info in MOVES.items():
        if info.get('category') != 'intermediate':
            continue

        duration = info['duration'] + 0.9
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


def posture_after(move_name):
    info = MOVES.get(move_name, {})
    prod = info.get('produces')
    if prod == 'sitting':
        return False
    return True  # standing, crouching, None  treat as standing


def posture_before(move_name):
    info = MOVES.get(move_name, {})
    req = info.get('requires')
    if req == 'sitting':
        return False
    if req == 'standing':
        return True
    return None  # no strict requirement


# ---------------------------------------------------------------------------------------
# STABILIZATION LOGIC (Option A)
# ---------------------------------------------------------------------------------------

def stabilize():
    """Bring NAO to a stable posture before/after each move."""
    try:
        motionProxy.wbEnable(False)               # disable whole-body balancing
        motionProxy.setStiffnesses("Body", 1.0)   # keep robot stable
        postureProxy.goToPosture("StandInit", 0.7)
        time.sleep(0.3)
    except Exception as e:
        print("[WARN] Stabilization issue:", e)


def run_move(move_name):
    if move_name not in moves:
        print("[ERROR] Move not found:", move_name)
        return

    print("[STABILIZING BEFORE]", move_name)
    stabilize()

    print("[RUNNING]", move_name)
    moves[move_name](ip, port)

    print("[STABILIZING AFTER]", move_name)
    stabilize()


def measure_move_time(move_name, ip, port):
    if move_name not in moves:
        print("[ERROR] Move not found:", move_name)
        return 0.0

    stabilize()

    print("[MEASURE]", move_name)
    start = time.time()
    try:
        moves[move_name](ip, port)
    except Exception as e:
        print("[ERROR during execution of %s] %s" % (move_name, e))
        return 0.0
    end = time.time()

    stabilize()
    return end - start


# ---------------------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------------------

def main():
    global postureProxy, motionProxy
    postureProxy = ALProxy("ALRobotPosture", ip, port)
    motionProxy = ALProxy("ALMotion", ip, port)

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

    mandatory_moves = []
    for name in mandatory_order:
        info = MOVES[name]
        mandatory_moves.append((name, Move(info['duration'] + 0.9)))

    intermediate_moves = build_intermediate_moves()

    total_mand_time = sum(m[1].duration for m in mandatory_moves)
    if total_mand_time > MAX_TIME:
        print("ERROR: mandatory moves exceed time limit.")
        return

    segments = len(mandatory_moves) - 1
    time_for_intermediates = MAX_TIME - total_mand_time

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

    per_segment_time = (time_for_intermediates / standing_segments) if standing_segments > 0 else 0

    print("Planning choreography...")
    print("Total mandatory time: %.2f s, remaining: %.2f s"
          % (total_mand_time, time_for_intermediates))

    full_choreo = ()
    total_intermediate_moves = 0

    for idx in range(1, len(mandatory_moves)):
        start_name = mandatory_moves[idx - 1][0]
        end_name = mandatory_moves[idx][0]

        print(" Segment %d: %s -> %s" % (idx, start_name, end_name))
        required_moves = 1 if segment_is_standing[idx - 1] else 0
        segment_time = per_segment_time if required_moves else 0

        if required_moves == 0:
            if idx == 1:
                full_choreo += (start_name,)
            full_choreo += (end_name,)
            print("  -> no intermediates.")
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
            print("  -> No solution found.")
            if idx == 1:
                full_choreo += (start_name,)
            full_choreo += (end_name,)
            continue

        sol_dict = from_state_to_dict(solution_node.state)
        seg_choreo = sol_dict['choreography']

        if idx == 1:
            full_choreo += seg_choreo
        else:
            full_choreo += seg_choreo[1:]

        total_intermediate_moves += sol_dict['moves_done']

        if full_choreo[-1] != end_name:
            full_choreo += (end_name,)

        print("  -> segment choreography:", " -> ".join(seg_choreo))

    print("\nFinal choreography:")
    print(" -> ".join(full_choreo))

    total_time = sum(MOVES[m]['duration'] + 0.9 for m in full_choreo)
    print("\nTotal time: %.2f s (MAX = %.2f)" % (total_time, MAX_TIME))
    print("Total intermediate moves used:", total_intermediate_moves)

    print("\n REAL EXECUTION TIMING")

    real_total = 0.0
    for move_name in full_choreo:
        dt = measure_move_time(move_name, ip, port)
        real_total += dt
        print("  %s : %.2f s" % (move_name, dt))

    print("\nREAL total execution time: %.2f s" % real_total)


if __name__ == "__main__":
    main()
'''