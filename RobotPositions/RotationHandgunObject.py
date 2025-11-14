# Movimento Completo: Inserimento Ventaglio e Rotazione Braccio Destro

import sys
import motion
import time
from naoqi import ALProxy

def main(robotIP, port):

    # Init proxies
    try:
        motionProxy = ALProxy("ALMotion", robotIP, port)
    except Exception, e:
        print "Could not create proxy to ALMotion"
        print "Error was:", e

    try:
        postureProxy = ALProxy("ALRobotPosture", robotIP, port)
    except Exception, e:
        print "Could not create proxy to ALRobotPosture"
        print "Error was:", e

    try:
        ttsProxy = ALProxy("ALTextToSpeech", robotIP, port)
    except Exception, e:
        print "Could not create proxy to ALTextToSpeech"
        print "Error was:", e

    time.sleep(1)

    # Helper: degrees -> radians
    def rad(d):
        return d * 3.14159 / 180.0

    # ------------------------------------------------------------
    # 1) INITIAL ARM POSITION
    # ------------------------------------------------------------
    R = dict(ShoulderPitch=67.7, ShoulderRoll=-26.4,
             ElbowYaw=90.9, ElbowRoll=88.5,
             WristYaw=80, Hand=0.35)

    L = dict(ShoulderPitch=78.0, ShoulderRoll=16.6,
             ElbowYaw=-68.3, ElbowRoll=-49.2,
             WristYaw=4.3, Hand=0.0)

    # Left Arm
    motionProxy.post.angleInterpolation(
        "LArm",
        [rad(L["ShoulderPitch"]), rad(L["ShoulderRoll"]), rad(L["ElbowYaw"]),
         rad(L["ElbowRoll"]), rad(L["WristYaw"]), L["Hand"]],
        1,
        True
    )

    # Right Arm
    motionProxy.post.angleInterpolation(
        "RArm",
        [rad(R["ShoulderPitch"]), rad(R["ShoulderRoll"]), rad(R["ElbowYaw"]),
         rad(R["ElbowRoll"]), rad(R["WristYaw"]), R["Hand"]],
        1,
        True
    )

    time.sleep(1)

    # ------------------------------------------------------------
    # 2) OPEN RIGHT HAND (Ask user to insert fan)
    # ------------------------------------------------------------
    motionProxy.angleInterpolation("RHand", [0.90], 1, True)
    time.sleep(1)

    # ------------------------------------------------------------
    # 3) CLOSE RIGHT HAND (fan grasped)
    # ------------------------------------------------------------
    motionProxy.angleInterpolation("RHand", [0.05], 1, True)
    time.sleep(0.5)

    # ------------------------------------------------------------
    # 4) ROTATE FAN (Right Wrist rotation only)
    # ------------------------------------------------------------
    R = dict(ShoulderPitch=67.7, ShoulderRoll=-26.4,
             ElbowYaw=90.9, ElbowRoll=88.5,
             WristYaw=60, Hand=0.10)

    motionProxy.angleInterpolation(
        "RArm",
        [rad(R["ShoulderPitch"]), rad(R["ShoulderRoll"]), rad(R["ElbowYaw"]),
         rad(R["ElbowRoll"]), rad(R["WristYaw"]), R["Hand"]],
        1,
        True
    )


if __name__ == "__main__":

    robotIP = "127.0.0.1"
    port = 9559

    if len(sys.argv) >= 2:
        robotIP = sys.argv[1]
    if len(sys.argv) >= 3:
        port = int(sys.argv[2])

    main(robotIP, port)
