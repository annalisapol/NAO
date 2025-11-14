import sys, os, time, yaml
from load_moves import load_robot_moves
from constants import *

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

pythonpath = config["pythonpath"]
ip = config["robot"]["ip"]
port = config["robot"]["port"]

if pythonpath not in sys.path:
    sys.path.append(pythonpath)

from naoqi import ALProxy

motion = ALProxy("ALMotion", ip, port)
posture = ALProxy("ALRobotPosture", ip, port)
bm = ALProxy("ALBehaviorManager", ip, port)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROBOT_POSITIONS = os.path.join(BASE_DIR, "RobotPositions")

moves = load_robot_moves(ROBOT_POSITIONS)


def run_move(move_name):
    if move_name not in moves:
        print("[ERROR] Move not found:", move_name)
        return

    print("[RUNNING]", move_name)
    moves[move_name](ip, port)


"""
CONSTRAINTS:
- possible incompatibilities between two consecutive positions (use
simulator in choreographe to understand if and what they are)
- time constraints (2 minutes max for the whole choreography)
- constraints on the number of intermediate positions to be used in the
whole choreography (at least 5)
"""