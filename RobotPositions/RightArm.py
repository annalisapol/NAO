# Movimento Completo Rotazione Braccio Destro

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

    # Helper for degrees → radians
    def rad(deg):
        return deg * 3.14159 / 180.0

    # ------------------------------------------------------------
    # 1) START POSITION (both arms symmetric)
    # ------------------------------------------------------------
    R = dict(ShoulderPitch=78.0, ShoulderRoll=-16.6,
             ElbowYaw=68.3, ElbowRoll=49.2,
             WristYaw=4.3, Hand=0.10)

    L = dict(ShoulderPitch=78.0, ShoulderRoll=16.6,
             ElbowYaw=-68.3, ElbowRoll=-49.2,
             WristYaw=4.3, Hand=0.0)

    motionProxy.post.angleInterpolation(
        "LArm",
        [rad(L["ShoulderPitch"]), rad(L["ShoulderRoll"]), rad(L["ElbowYaw"]),
         rad(L["ElbowRoll"]), rad(L["WristYaw"]), L["Hand"]],
        2,
        True
    )

    motionProxy.angleInterpolation(
        "RArm",
        [rad(R["ShoulderPitch"]), rad(R["ShoulderRoll"]), rad(R["ElbowYaw"]),
         rad(R["ElbowRoll"]), rad(R["WristYaw"]), R["Hand"]],
        2,
        True
    )

    # ------------------------------------------------------------
    # 2) MOVEMENT: open and extend RArm
    # ------------------------------------------------------------
    R = dict(ShoulderPitch=-75.7, ShoulderRoll=-79.8,
             ElbowYaw=-57.6, ElbowRoll=2.2,
             WristYaw=87.0, Hand=0.35)

    motionProxy.setAngles(
        "RArm",
        [rad(R["ShoulderPitch"]), rad(R["ShoulderRoll"]), rad(R["ElbowYaw"]),
         rad(R["ElbowRoll"]), rad(R["WristYaw"]), R["Hand"]],
        0.1
    )

    time.sleep(2)

    # ------------------------------------------------------------
    # 3) Raise RArm sideways
    # ------------------------------------------------------------
    R = dict(ShoulderPitch=-79.8, ShoulderRoll=-26.2,
             ElbowYaw=-57.6, ElbowRoll=2.2,
             WristYaw=87.0, Hand=0.35)

    motionProxy.setAngles(
        "RArm",
        [rad(R["ShoulderPitch"]), rad(R["ShoulderRoll"]), rad(R["ElbowYaw"]),
         rad(R["ElbowRoll"]), rad(R["WristYaw"]), R["Hand"]],
        0.15
    )

    time.sleep(1)

    # ------------------------------------------------------------
    # 4) Align shoulder and move RArm forward
    # ------------------------------------------------------------
    R = dict(ShoulderPitch=11.0, ShoulderRoll=5.4,
             ElbowYaw=68.3, ElbowRoll=2.2,
             WristYaw=88.5, Hand=0.35)

    motionProxy.angleInterpolation(
        "RArm",
        [rad(R["ShoulderPitch"]), rad(R["ShoulderRoll"]), rad(R["ElbowYaw"]),
         rad(R["ElbowRoll"]), rad(R["WristYaw"]), R["Hand"]],
        4,
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
