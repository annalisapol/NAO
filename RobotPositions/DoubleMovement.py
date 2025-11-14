# Movimento Completo Movimento Doppio

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

    # Helper: degrees → radians
    def rad(d):
        return d * 3.14159 / 180.0

    # ------------------------------------------------------------
    # 1) INITIAL POSITION
    # ------------------------------------------------------------
    R = dict(ShoulderPitch=78.0, ShoulderRoll=-39.9,
             ElbowYaw=68.3, ElbowRoll=57.2,
             WristYaw=95, Hand=0.10)

    L = dict(ShoulderPitch=78.0, ShoulderRoll=39.9,
             ElbowYaw=-68.3, ElbowRoll=-57.2,
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

    time.sleep(0.5)

    # ------------------------------------------------------------
    # 2) MOVEMENT PART 1 (rotation movement)
    # ------------------------------------------------------------
    R = dict(ShoulderPitch=77.7, ShoulderRoll=-39.5,
             ElbowYaw=33.7, ElbowRoll=70,
             WristYaw=95, Hand=0.10)

    L = dict(ShoulderPitch=77.8, ShoulderRoll=49.2,
             ElbowYaw=-68.5, ElbowRoll=-9.4,
             WristYaw=4.5, Hand=0.0)

    motionProxy.setAngles(
        "RArm",
        [rad(R["ShoulderPitch"]), rad(R["ShoulderRoll"]), rad(R["ElbowYaw"]),
         rad(R["ElbowRoll"]), rad(R["WristYaw"]), R["Hand"]],
        0.05
    )

    time.sleep(0.2)

    motionProxy.setAngles(
        "LArm",
        [rad(L["ShoulderPitch"]), rad(L["ShoulderRoll"]), rad(L["ElbowYaw"]),
         rad(L["ElbowRoll"]), rad(L["WristYaw"]), L["Hand"]],
        0.08
    )

    time.sleep(1.2)

    # ------------------------------------------------------------
    # 3) MOVEMENT PART 2 (arms parallel to the floor)
    # ------------------------------------------------------------
    R = dict(ShoulderPitch=15.1, ShoulderRoll=-10.6,
             ElbowYaw=9.5, ElbowRoll=70,
             WristYaw=95, Hand=0.10)

    L = dict(ShoulderPitch=77.8, ShoulderRoll=75.8,
             ElbowYaw=-68.5, ElbowRoll=-2.5,
             WristYaw=4.5, Hand=0.0)

    motionProxy.setAngles(
        "RArm",
        [rad(R["ShoulderPitch"]), rad(R["ShoulderRoll"]), rad(R["ElbowYaw"]),
         rad(R["ElbowRoll"]), rad(R["WristYaw"]), R["Hand"]],
        0.15
    )

    time.sleep(0.3)

    motionProxy.setAngles(
        "LArm",
        [rad(L["ShoulderPitch"]), rad(L["ShoulderRoll"]), rad(L["ElbowYaw"]),
         rad(L["ElbowRoll"]), rad(L["WristYaw"]), L["Hand"]],
        0.1
    )

    time.sleep(0.6)

    # ------------------------------------------------------------
    # 4) FINAL POSITION
    # ------------------------------------------------------------
    R = dict(ShoulderPitch=62.4, ShoulderRoll=-15.7,
             ElbowYaw=51.7, ElbowRoll=81,
             WristYaw=105, Hand=0.10)

    L = dict(ShoulderPitch=27.0, ShoulderRoll=29.8,
             ElbowYaw=-72.9, ElbowRoll=-27.2,
             WristYaw=4.5, Hand=0.0)

    motionProxy.post.angleInterpolation(
        "RArm",
        [rad(R["ShoulderPitch"]), rad(R["ShoulderRoll"]), rad(R["ElbowYaw"]),
         rad(R["ElbowRoll"]), rad(R["WristYaw"]), R["Hand"]],
        1.4,
        True
    )

    time.sleep(0.3)

    motionProxy.angleInterpolation(
        "LArm",
        [rad(L["ShoulderPitch"]), rad(L["ShoulderRoll"]), rad(L["ElbowYaw"]),
         rad(L["ElbowRoll"]), rad(L["WristYaw"]), L["Hand"]],
        1.4,
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
