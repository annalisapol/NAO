import sys, time, yaml

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

pythonpath = config["pythonpath"]
ip = config["robot"]["ip"]
port = config["robot"]["port"]

if pythonpath not in sys.path:
    sys.path.append(pythonpath)


from naoqi import ALProxy

motion = ALProxy("ALMotion", ip, port)
posture = ALProxy("ALRobotPosture", ip, port)

max_time = 120 

motion.wakeUp()

moves = ["RotationHandgunObject", "RightArm", "DoubleMovement", "ArmsOpening", "UnionArms", "Crouch", "MoveForward", "MoveBackward", "DiagonalLeft", "DiagonalRight", "Stand", "RotationFootRLeg", "RotationFootLLeg", "StandInit", "StandZero", "Sit", "SitRelax"]

sequence = ["StandInit", "StandZero", "Crouch", "StandInit"]

for pose in sequence:
    print("Going to posture:", pose)
    posture.goToPosture(pose, 0.7)

motion.rest()




