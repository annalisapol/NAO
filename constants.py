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
