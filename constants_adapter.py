# -*- coding: utf-8 -*-
from constants import MOVES

def conv_requires(req):
    if req == "standing": return True
    if req == "sitting": return False
    return None

def conv_produces(prod):
    if prod == "standing": return True
    if prod == "sitting": return False
    if prod == "crouching": return False
    return None

intermediatePos = {}
for name, info in MOVES.items():
    if info["category"] == "intermediate":
        pre = {"isStanding": conv_requires(info["requires"])}
        post = {"isStanding": conv_produces(info["produces"])}
        dur = info["duration"]
        intermediatePos[name] = [pre, post, dur]

mandatoryPos = []
for name, info in MOVES.items():
    if info["category"] == "mandatory":
        pre = conv_requires(info["requires"])
        post = conv_produces(info["produces"])
        dur = info["duration"]
        mandatoryPos.append((name, [pre, post, dur]))

initialPos = (
    "StandInit",
    [
        conv_requires(MOVES["StandInit"]["requires"]),
        conv_produces(MOVES["StandInit"]["produces"]),
        MOVES["StandInit"]["duration"]
    ]
)

goalPos = (
    "Crouch",
    [
        conv_requires(MOVES["Crouch"]["requires"]),
        conv_produces(MOVES["Crouch"]["produces"]),
        MOVES["Crouch"]["duration"]
    ]
)

totalMandatory = [initialPos] + mandatoryPos + [goalPos]
