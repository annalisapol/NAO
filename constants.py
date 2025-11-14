MOVES = ['ArmDanceDX', 'ArmDanceSX', 'ArmsOpening', 'BirthdayDance', 'BlowKisses', 'Crouch', 'DanceMove', 'DiagonalLeft', 'DiagonalRight', 'Disco', 'DoubleMovement', 'Hello', 'MoveBackward', 'MoveForward', 'RightArm', 'RotationFeet', 'RotationFootLLeg', 'RotationFootRLeg', 'RotationHandgunObject', 'Sit', 'SitRelax', 'Sprinkler1', 'Sprinkler2', 'Stand', 'StandInit', 'StandZero', 'ThrillerArmSideways', 'ThrillerClap', 'ThrillerSnapSnap', 'UnionArms', 'VOnEyes', 'WipeForehead']
mandatory_positions = ["Sit", "SitRelax", "WipeForehead", "Stand", "Hello", "StandZero"]
INITIAL_STATE = "StandInit"
FINAL_GOAL = "Crouch"

MAX_TIME = 120

MAX_SPEED = 1.0 # maximum speed for NAO using applyPosture()

MOVE_TIME = {"SitRelax": 11.6,
"Sit": 13.2,
"RotationFootRLeg": 97.9,
"StandInit": 0.76,
"ThrillerClap": 6.64,
"RotationHandgunObject": 5.43,
"Sprinkler2": 6.58,
"MoveForward": 3.94,
"Sprinkler1": 6.65,
"Crouch": 3.1,
"ThrillerSnapSnap": 6.71,
"MoveBackward": 4.5,
"RotationFeet": 8.93,
"ArmDanceDX": 6.55,
"DiagonalLeft": 3.36,
"ArmsOpening": 6.87,
"DanceMove": 11.94,
"ThrillerArmSideways": 6.63,
"Disco": 6.61,
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
"BlowKisses": 12.57,
"UnionArms": 10.13}