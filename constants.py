MOVES = ['ArmDanceDX', 'ArmDanceSX', 'ArmsOpening', 'BirthdayDance', 'BlowKisses', 'Crouch', 'DanceMove', 'DiagonalLeft', 'DiagonalRight', 'Disco', 'DoubleMovement', 'Hello', 'MoveBackward', 'MoveForward', 'RightArm', 'RotationFeet', 'RotationFootLLeg', 'RotationFootRLeg', 'RotationHandgunObject', 'Sit', 'SitRelax', 'Sprinkler1', 'Sprinkler2', 'Stand', 'StandInit', 'StandZero', 'ThrillerArmSideways', 'ThrillerClap', 'ThrillerSnapSnap', 'UnionArms', 'VOnEyes', 'WipeForehead']mandatory_positions = ["Sit", "SitRelax", "WipeForehead", "Stand", "Hello", "StandZero"]
INITIAL_STATE = "StandInit"
FINAL_GOAL = "Crouch"

MAX_TIME = 120

MAX_SPEED = 1.0 # maximum speed for NAO using applyPosture()