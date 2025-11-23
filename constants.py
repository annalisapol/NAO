# Changing the data retrieving system, it was getting messy
# Keeping the code if we need to revert
# Creating one dictionary with all the moves information (time, pre/post conditions, categories ..)
# It' a bit long but we only have 26 moves and it's easier to read/retrieve this way

MAX_TIME = 120

MOVES = {
    'ArmDanceDX': {
        "category": "intermediate",
        "duration": 5.55,
        "requires": "standing",
        "produces": "standing",
        "module": "ArmDanceDX"
    },
    'ArmDanceSX': {
        "category": "intermediate",
        "duration": 5.56,
        "requires": "standing",
        "produces": "standing",
        "module": "ArmDanceSX"
    },
    'ArmsOpening': {
        "category": "intermediate",
        "duration": 6.87,
        "requires": "standing",
        "produces": "standing",
        "module": "ArmsOpening"
    },
    'BirthdayDance': {
        "category": "intermediate",
        "duration": 13.47,
        "requires": "standing",
        "produces": "standing",
        "module": "BirthdayDance"
    },
    'DiagonalLeft': {
        "category": "intermediate",
        "duration": 4.36,
        "requires": "standing",
        "produces": "standing",
        "module": "DiagonalLeft"
    },
    'DiagonalRight': {
        "category": "intermediate",
        "duration": 4.38,
        "requires": "standing",
        "produces": "standing",
        "module": "DiagonalRight"
    },
    'Disco': {
        "category": "intermediate",
        "duration": 6.61,
        "requires": "standing",
        "produces": "standing",
        "module": "Disco"
    },
    'DoubleMovement': {
        "category": "intermediate",
        "duration": 7.26,
        "requires": "standing",
        "produces": "standing",
        "module": "DoubleMovement"
    },
    'MoveBackward': {
        "category": "intermediate",
        "duration": 4.5,
        "requires": "standing",
        "produces": "standing",
        "module": "MoveBackward"
    },
    'MoveForward': {
        "category": "intermediate",
        "duration": 5,
        "requires": "standing",
        "produces": "standing",
        "module": "MoveForward"
    },
    'RightArm': {
        "category": "intermediate",
        "duration": 13.33,
        "requires": "standing",
        "produces": "standing",
        "module": "RightArm"
    },
    'RotationFootLLeg': {
        "category": "intermediate",
        "duration": 14.35,
        "requires": "standing",
        "produces": "standing",
        "module": "RotationFootLLeg"
    },
    'RotationFootRLeg': {
        "category": "intermediate",
        "duration": 97.9,
        "requires": "standing",
        "produces": "standing",
        "module": "RotationFootRLeg"
    },
    'RotationHandgunObject': {
        "category": "intermediate",
        "duration": 6.43,
        "requires": "standing",
        "produces": "standing",
        "module": "RotationHandgunObject"
    },
    'Sprinkler1': {
        "category": "intermediate",
        "duration": 5.65,
        "requires": "standing",
        "produces": "standing",
        "module": "Sprinkler1"
    },
    'Sprinkler2': {
        "category": "intermediate",
        "duration": 5.58,
        "requires": "standing",
        "produces": "standing",
        "module": "Sprinkler2"
    },
    'UnionArms': {
        "category": "intermediate",
        "duration": 11.13,
        "requires": "standing",
        "produces": "standing",
        "module": "UnionArms"
    },
    'VOnEyes': {
        "category": "intermediate",
        "duration": 6.74,
        "requires": "standing",
        "produces": "standing",
        "module": "VOnEyes"
    },
    "Sit": {
        "category": "mandatory",
        "duration": 11.2,
        "requires": "standing",
        "produces": "sitting",
        "module": "Sit"
    },
    "WipeForehead": {
        "category": "mandatory",
        "duration": 8.96,
        "requires": "standing",
        "produces": "standing",
        "module": "WipeForehead"
    },
    "Hello": {
        "category": "mandatory",
        "duration": 8.68,
        "requires": "standing",
        "produces": "standing",
        "module": "Hello"
    },
    "SitRelax": {
        "category": "mandatory",
        "duration": 12.6,
        "requires": "standing",
        "produces": "sitting",
        "module": "SitRelax"
    },
    "Stand": {
        "category": "mandatory",
        "duration": 1.82,
        "requires": "sitting",
        "produces": "standing",
        "module": "Stand"
    },
    "StandZero": {
        "category": "mandatory",
        "duration": 1.25,
        "requires": "standing",
        "produces": "standing",
        "module": "StandZero"
    },
    "StandInit": {
        "category": "starting",
        "duration": 1.76,
        "requires": "standing",   # adjust if needed
        "produces": "standing",
        "module": "StandInit"
    },
    "Crouch": {
        "category": "ending",
        "duration": 4.1,
        "requires": "standing",   # adjust if needed
        "produces": "crouching",   
        "module": "Crouch"
    }
}

"""
INTERMEDIATE = ['ArmDanceDX', 'ArmDanceSX', 'ArmsOpening', 'BirthdayDance', 'BlowKisses',  'DanceMove', 'DiagonalLeft', 'DiagonalRight', 'Disco', 'DoubleMovement', 'MoveBackward', 'MoveForward', 'RightArm', 'RotationFeet', 'RotationFootLLeg', 'RotationFootRLeg', 'RotationHandgunObject', 'Sprinkler1', 'Sprinkler2',  'ThrillerArmSideways', 'ThrillerClap', 'ThrillerSnapSnap', 'UnionArms', 'VOnEyes']
MANDATORY = ["Sit", "WipeForehead", "Hello", "SitRelax", "Stand", "StandZero"]
INITIAL_STATE_M = "StandInit"
FINAL_GOAL_M = "Crouch"


MAX_TIME = 120

MOVE_TIME = {"SitRelax": 11.6,
"Sit": 13.2,
"RotationFootRLeg": 97.9,
"StandInit": 0.76,
"RotationHandgunObject": 5.43,
"Sprinkler2": 6.58,
"MoveForward": 3.94,
"Sprinkler1": 6.65,
"Crouch": 3.1,
"MoveBackward": 4.5,
"ArmDanceDX": 6.55,
"Disco": 6.61,
"DiagonalLeft": 3.36,
"ArmsOpening": 6.87,
"VOnEyes": 7.74,
"Stand": 0.82,
"ArmDanceSX": 6.56,
"DiagonalRight": 3.38,
"StandZero": 1.25,
"Hello": 7.68,
"DoubleMovement": 7.26,
"RightArm": 12.33,
"WipeForehead": 7.96,
"RotationFootLLeg": 13.35,
"BirthdayDance": 12.47,
"UnionArms": 10.13}

MOVE_CONDITIONS = {}

SITTING_MOVES = ["Sit", "SitRelax", "Crouch"]

for move in SITTING_MOVES:
    MOVE_CONDITIONS[move] = {
        "requires": None,
        "produces": "sitting"
    }

STANDING_MOVES = [
    'ArmDanceDX', 'ArmDanceSX', 'ArmsOpening', 'BirthdayDance',
    'BlowKisses', 'DanceMove', 'DiagonalLeft', 'DiagonalRight', 
    'Disco', 'DoubleMovement', 'Hello', 'MoveBackward', 'MoveForward', 
    'RightArm', 'RotationFeet', 'RotationFootLLeg', 'RotationFootRLeg', 
    'RotationHandgunObject', 'Sprinkler1', 'Sprinkler2', 
    'Stand', 'StandInit', 'StandZero', 
    'ThrillerArmSideways', 'ThrillerClap', 'ThrillerSnapSnap', 
    'UnionArms', 'VOnEyes', 'WipeForehead'
]

for move in STANDING_MOVES:
    MOVE_CONDITIONS[move] = {
        "requires": None,
        "produces": "standing"
    }
"""