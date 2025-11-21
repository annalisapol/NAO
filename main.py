# -*- coding: utf-8 -*-
import subprocess
import sys
from search import astar_search
from naoPlanning import NaoProblem
from constants import MOVES, MAX_TIME

def nao_dance(moves, robotIP, port):
    for m in moves:
        cmd = "python2 RobotPositions/{0}.py {1} {2}".format(m, robotIP, port)
        print("Move:", m)
        subprocess.Popen(cmd.split()).communicate()

def main(robotIP, port):

    # ---------- Build the initial state ----------
    init_state = {
        "pose": "StandInit",
        "isStanding": True,
        "time_used": MOVES["StandInit"]["duration"],
        "done_mandatory": frozenset()
    }

    # dummy goal placeholder (NaoProblem ignores self.goal)
    goal_state = None

    problem = NaoProblem(init_state, goal_state)

    print("[INFO] Running A* search...")
    res_node = astar_search(problem)

    if res_node is None:
        print("[ERROR] No plan found.")
        return

    # ---------- Extract action sequence ----------
    plan = res_node.path()
    moves = [node.state["pose"] for node in plan]

    # remove the first pose (StandInit) so we don't execute it
    moves = moves[1:]

    print("\n[PLAN FOUND]")
    for m in moves:
        print(" -", m)

    # ---------- Execute moves on the NAO ----------
    nao_dance(moves, robotIP, port)


if __name__ == "__main__":
    robotIP = "127.0.0.1"
    port = 36803
    main(robotIP, port)
