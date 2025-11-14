import sys, os, time, yaml
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
sys.path.append(ROBOT_POSITIONS)

from MoveForward import main as move_forward_main
from WipeForehead import main as wipe_forehead_main
from RotationFootLLeg import main as rotation_foot_LLeg_main

print("Available behaviors:")
print(bm.getInstalledBehaviors())


print("Postures available:")
print(posture.getPostureList())

print("Running MoveForward...")

rotation_foot_LLeg_main(ip, port)
move_forward_main(ip, port)
wipe_forehead_main(ip, port)
"""
CONSTRAINTS:
- possible incompatibilities between two consecutive positions (use
simulator in choreographe to understand if and what they are)
- time constraints (2 minutes max for the whole choreography)
- constraints on the number of intermediate positions to be used in the
whole choreography (at least 5)
"""