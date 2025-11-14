# load_moves.py
import os
import sys
import importlib

def load_robot_moves(folder_path):
    moves = {}

    if folder_path not in sys.path:
        sys.path.append(folder_path)

    for filename in os.listdir(folder_path):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = filename[:-3] 
            try:
                module = importlib.import_module(module_name)

                if hasattr(module, "main"):
                    moves[module_name] = module.main
                else:
                    print("[WARN] Module {} has no 'main' function".format(module_name))

            except Exception as e:
                print("[ERROR] Failed to import {}: {}".format(module_name, e))

    return moves

"""
returns something like:
{
    "MoveForward": <function MoveForward.main>,
    "WipeForehead": <function WipeForehead.main>,
    "DiagonalLeft": <function DiagonalLeft.main>,
    ...
}
"""