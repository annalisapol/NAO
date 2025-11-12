MOVES = ["RotationHandgunObject", "RightArm", "DoubleMovement", "ArmsOpening", "UnionArms", "Crouch", "MoveForward", "MoveBackward", "DiagonalLeft", "DiagonalRight", "Stand", "RotationFootRLeg", "RotationFootLLeg", "StandInit", "StandZero", "Sit", "SitRelax"]
mandatory_positions = ["Sit", "SitRelax", "WipeForehead", "Stand", "Hello", "StandZero"]
INITIAL_STATE = "StandInit"
FINAL_GOAL = "Crouch"

MAX_TIME = 120

MAX_SPEED = 1.0 # maximum speed for NAO using applyPosture()