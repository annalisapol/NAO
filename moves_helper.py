# -*- coding: utf-8 -*-
import os
import sys
import importlib
from constants import MOVES

# Changing this to reflect the new MOVES dict structure

# Loads the Python main() functions for all moves defined in MOVES

def load_moves(folder_path):
    moves = {}

    if folder_path not in sys.path:
        sys.path.append(folder_path)

    for move_name, info in MOVES.items():
        module_name = info["module"]   # for example name "SitInit" from the dict

        try:
            module = importlib.import_module(module_name)

            if hasattr(module, "main"):
                moves[move_name] = module.main
            else:
                print("[WARN] Module '%s' has no main() function." % module_name)

        except Exception as e:
            print("[ERROR] Could not import module '%s': %s" % (module_name, e))

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

# fast getters
def get_moves_names():
    return list(MOVES.keys())

def get_mandatory_moves():
    return [m for m in MOVES if MOVES[m]["category"] == "mandatory"]

def get_intermediate_moves():
    return [m for m in MOVES if MOVES[m]["category"] == "intermediate"]

def moves_requiring(posture):
    return [m for m, data in MOVES.items() if data["requires"] == posture]

def moves_producing(posture):
    return [m for m, data in MOVES.items() if data["produces"] == posture]

