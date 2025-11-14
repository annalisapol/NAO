# Movimento Completo: Unire le braccia

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

    time.sleep(1)

    # Helper: degrees -> radians
    def rad(deg):
        return deg * 3.14159 / 180.0

    # ------------------------------------------------------------
    # 1) START POSITION
    # ------------------------------------------------------------
    R = dict(ShoulderPitch=67.7, ShoulderRoll=-26.4,
             ElbowYaw=90.9, ElbowRoll=88.5,
             WristYaw=59.2, Hand=0.35)

    L = dict(ShoulderPitch=80.2, ShoulderRoll=24.1,
             ElbowYaw=-90.0, ElbowRoll=-4.4,
             WristYaw=0.5, Hand=0.0)

    motionProxy.post.angleInterpolation(
        "LArm",
        [rad(L["ShoulderPitch"]), rad(L["ShoulderRoll"]), rad(L["ElbowYaw"]),
         rad(L["ElbowRoll"]), rad(L["WristYaw"]), L["Hand"]],
        1,
        True
    )

    motionProxy.angleInterpolation(
        "RArm",
        [rad(R["ShoulderPitch"]), rad(R["ShoulderRoll"]), rad(R["ElbowYaw"]),
         rad(R["ElbowRoll"]), rad(R["WristYaw"]), R["Hand"]],
        1,
        True
    )

    time.sleep(0.2)

    # ------------------------------------------------------------
    # 2) OPEN / EXTEND ARMS
    # ------------------------------------------------------------
    R = dict(ShoulderPitch=58.8, ShoulderRoll=-25.9,
             ElbowYaw=90.6, ElbowRoll=25.0,
             WristYaw=3.2, Hand=0.35)

    L = dict(ShoulderPitch=58.8, ShoulderRoll=25.9,
             ElbowYaw=-90.6, ElbowRoll=-25.0,
             WristYaw=-59.4, Hand=0.0)

    motionProxy.post.angleInterpolation(
        "LArm",
        [rad(L["ShoulderPitch"]), rad(L["ShoulderRoll"]), rad(L["ElbowYaw"]),
         rad(L["ElbowRoll"]), rad(L["WristYaw"]), L["Hand"]],
        3,
        True
    )

    motionProxy.angleInterpolation(
        "RArm",
        [rad(R["ShoulderPitch"]), rad(R["ShoulderRoll"]), rad(R["ElbowYaw"]),
         rad(R["ElbowRoll"]), rad(R["WristYaw"]), R["Hand"]],
        2,
        True
    )

    # Rotate RWristYaw
    motionProxy.post.angleInterpolation(
        "RWristYaw",
        rad(59.4),
        1,
        True
    )

    time.sleep(0.5)

    # ------------------------------------------------------------
    # 3) CLOSE ARMS (Symmetric closing motion)
    # ------------------------------------------------------------
    R = dict(ShoulderPitch=45.9, ShoulderRoll=15.3,
             ElbowYaw=90.9, ElbowRoll=21.6,
             WristYaw=R["WristYaw"], Hand=R["Hand"])

    L = dict(ShoulderPitch=45.9, ShoulderRoll=-15.3,
             ElbowYaw=-90.0, ElbowRoll=-21.6,
             WristYaw=L["WristYaw"], Hand=L["Hand"])

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

    time.sleep(1)

    # ------------------------------------------------------------
    # 4) FINAL POSITION (Return to initial pose)
    # ------------------------------------------------------------
    R = dict(ShoulderPitch=78.0, ShoulderRoll=-16.6,
             ElbowYaw=68.3, ElbowRoll=49.2,
             WristYaw=4.3, Hand=0.35)

    L = dict(ShoulderPitch=78.0, ShoulderRoll=16.6,
             ElbowYaw=-68.3, ElbowRoll=-49.2,
             WristYaw=4.3, Hand=0.0)

    motionProxy.post.angleInterpolation(
        "LArm",
        [rad(L["ShoulderPitch"]), rad(L["ShoulderRoll"]), rad(L["ElbowYaw"]),
         rad(L["ElbowRoll"]), rad(L["WristYaw"]), L["Hand"]],
        1.5,
        True
    )

    motionProxy.angleInterpolation(
        "RArm",
        [rad(R["ShoulderPitch"]), rad(R["ShoulderRoll"]), rad(R["ElbowYaw"]),
         rad(R["ElbowRoll"]), rad(R["WristYaw"]), R["Hand"]],
        1.5,
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
