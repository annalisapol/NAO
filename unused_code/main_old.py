from nao_problem1 import NAOProblem
from search import *
from constants import MAX_TIME
from moves_helper import load_moves
import yaml, sys

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

pythonpath = config["pythonpath"]
ip = config["robot"]["ip"]
port = config["robot"]["port"]

if pythonpath not in sys.path:
    sys.path.append(pythonpath)

#create the problem
initial = "StandInit"
goal = "Crouch"
problem = NAOProblem()
#run search
print("TRY-1 ")

result_node = iterative_deepening_search(problem)
print("TRY- 2")

if result_node is None:
    print("No valid plan found")

    #sys.exit(0)
actions = []
node = result_node
'''
node.action      # the move taken from its parent
node.state       # the resulting state
node.parent      # pointer to the previous node
'''
print("TRY- 3")
print("Plan found:", result_node)
while node.parent is not None:
    actions.append(node.action)
    node = node.parent
actions.reverse()
print("Generated plan:")
for a in actions:
    print("->",a)
print("Total time: ", result_node.state["time"])
# extract +print actions
if __name__ == "__main__":
   # 1. Load move data
   moves = load_moves("RobotPositions/")
   move_durations = MAX_TIME
   pass


    # 2. Initialize search problem
    # 3. Run planner
    # 4. Print or execute plan
    
