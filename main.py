"""
This script runs the full choreography planning pipeline:

1. Load the domain information:
   - move durations
   - posture pre/post conditions
   - mandatory and intermediate move sets

2. Create the initial planning state and initialize the NAOProblem object.

3. Run the search algorithm (e.g., Uniform Cost Search, A*, BFS)
   to generate a valid dance sequence that:
      - completes all mandatory moves,
      - includes at least 5 intermediate moves,
      - stays within the 120-second limit,
      - respects posture constraints.

4. Extract the resulting plan (the sequence of moves) from the search node.

5. Optionally:
   - print the plan,
   - send each movement to the NAO robot for execution,
   - or save the result for later use.

This file acts as the entry point for planning and executing the NAO choreography.
"""
from constants import *
from nao_problem import NAOProblem
from moves_helper import load_moves
from naoqi import ALProxy

import sys, os, time, yaml
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

pythonpath = config["pythonpath"]
ip = config["robot"]["ip"]
port = config["robot"]["port"]

if pythonpath not in sys.path:
    sys.path.append(pythonpath)

if __name__ == "__main__":
   # 1. Load move data
   moves = load_moves("RobotPositions/")
   move_durations = MAX_TIME



    # 2. Initialize search problem
    # 3. Run planner
    # 4. Print or execute plan
    pass
