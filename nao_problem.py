from search import Problem
from constants import MOVES, MAX_TIME
from utils import distance

class NAOProblem(Problem):
    def __init__(self, initial, goal, move_durations, incompatibilities, max_time=MAX_TIME):
        self.super().__init___(initial, goal)
        self.max_time = max_time,
        self.move_durations = move_durations #should be a dict mapping each move to its duration in seconds, maybe at the fastest speed
        self.incompatibilities = incompatibilities #to be defined, should be a dict mapping each move to the list of incompatible moves

    def action(self, state):
        ...