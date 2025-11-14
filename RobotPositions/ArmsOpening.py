# Movimento Completo Apertura Braccia con Rotazione

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
        print "Error was: ", e

    try:
        postureProxy = ALProxy("ALRobotPosture", robotIP, port)
    except Exception, e:
        print "Could not create proxy to ALRobotPosture"
        print "Error was: ", e

    try:
        ttsProxy = ALProxy("ALTextToSpeech", robotIP, port)
    except Exception, e:
        print "Could not create proxy to ALTextToSpeech"
        print "Error was: ", e

    #time.sleep(1)

    # ---------------------------------------------------------------------------
    # Helper: convert degrees to radians
    # ---------------------------------------------------------------------------
    def rad(deg):
        return deg * 3.14159 / 180.0

    # ---------------------------------------------------------------------------
    # START POSITION
    # ---------------------------------------------------------------------------
    R = {
        "ShoulderPitch": 78.0, "ShoulderRoll": -16.6,
        "ElbowYaw": 68.3, "ElbowRoll": 49.2,
        "WristYaw": 4.3, "Hand": 0.10
    }

    L = {
        "ShoulderPitch": 78.0, "ShoulderRoll": 16.6,
        "ElbowYaw": -68.3, "ElbowRoll": -49.2,
        "WristYaw": 4.3, "Hand": 0.0
    }

    # Left arm
    motionProxy.post.angleInterpolation(
        "LArm",
        [rad(L["ShoulderPitch"]), rad(L["ShoulderRoll"]), rad(L["ElbowYaw"]),
         rad(L["ElbowRoll"]), rad(L["WristYaw"]), L["Hand"]],
        2,
        True
    )

    # Right arm
    motionProxy.angleInterpolation(
        "RArm",
        [rad(R["ShoulderPitch"]), rad(R["ShoulderRoll"]), rad(R["ElbowYaw"]),
         rad(R["ElbowRoll"]), rad(R["WristYaw"]), R["Hand"]],
        2,
        True
    )

    #time.sleep(0.2)

    # ---------------------------------------------------------------------------
    # MOVEMENT 1
    # ---------------------------------------------------------------------------
    R = {
        "ShoulderPitch": 24.9, "ShoulderRoll": 8.0,
        "ElbowYaw": 67.8, "ElbowRoll": 14.7,
        "WristYaw": 79.3, "Hand": 0.35
    }

    L = {
        "ShoulderPitch": 68.8, "ShoulderRoll": 14.3,
        "ElbowYaw": -68.4, "ElbowRoll": -53.9,
        "WristYaw": 4.5, "Hand": 0.0
    }

    motionProxy.setAngles(
        "LArm",
        [rad(L["ShoulderPitch"]), rad(L["ShoulderRoll"]), rad(L["ElbowYaw"]),
         rad(L["ElbowRoll"]), rad(L["WristYaw"]), L["Hand"]],
        0.08
    )

    motionProxy.setAngles(
        "RArm",
        [rad(R["ShoulderPitch"]), rad(R["ShoulderRoll"]), rad(R["ElbowYaw"]),
         rad(R["ElbowRoll"]), rad(R["WristYaw"]), R["Hand"]],
        0.08
    )

    #time.sleep(1.2)

    # ---------------------------------------------------------------------------
    # Close Arms
    # ---------------------------------------------------------------------------
    R = {
        "ShoulderPitch": 24.5, "ShoulderRoll": 16.9,
        "ElbowYaw": 67.4, "ElbowRoll": 14.9,
        "WristYaw": 79.1, "Hand": 0.35
    }

    L = {
        "ShoulderPitch": 66.7, "ShoulderRoll": -12.3,
        "ElbowYaw": -69.0, "ElbowRoll": -53.7,
        "WristYaw": 4.6, "Hand": 0.0
    }

    motionProxy.setAngles(
        "LArm",
        [rad(L["ShoulderPitch"]), rad(L["ShoulderRoll"]), rad(L["ElbowYaw"]),
         rad(L["ElbowRoll"]), rad(L["WristYaw"]), L["Hand"]],
        0.1
    )

    motionProxy.setAngles(
        "RArm",
        [rad(R["ShoulderPitch"]), rad(R["ShoulderRoll"]), rad(R["ElbowYaw"]),
         rad(R["ElbowRoll"]), rad(R["WristYaw"]), R["Hand"]],
        0.15
    )

    #time.sleep(0.4)

    # ---------------------------------------------------------------------------
    # Stretch + Raise Arms
    # ---------------------------------------------------------------------------
    R = {
        "ShoulderPitch": 24.7, "ShoulderRoll": -51.8,
        "ElbowYaw": 45.6, "ElbowRoll": 14.7,
        "WristYaw": 78.9, "Hand": 0.35
    }

    L = {
        "ShoulderPitch": 24.7, "ShoulderRoll": 51.8,
        "ElbowYaw": -45.6, "ElbowRoll": -14.7,
        "WristYaw": -78.9, "Hand": 0.0
    }

    motionProxy.setAngles(
        "RArm",
        [rad(R["ShoulderPitch"]), rad(R["ShoulderRoll"]), rad(R["ElbowYaw"]),
         rad(R["ElbowRoll"]), rad(R["WristYaw"]), R["Hand"]],
        0.1
    )

    #time.sleep(0.2)

    motionProxy.setAngles(
        "LArm",
        [rad(L["ShoulderPitch"]), rad(L["ShoulderRoll"]), rad(L["ElbowYaw"]),
         rad(L["ElbowRoll"]), rad(L["WristYaw"]), L["Hand"]],
        0.1
    )

    #time.sleep(2.2)

    # ---------------------------------------------------------------------------
    # FINAL POSITION
    # ---------------------------------------------------------------------------
    R = {
        "ShoulderPitch": 66.4, "ShoulderRoll": -26.1,
        "ElbowYaw": 106.0, "ElbowRoll": 80,
        "WristYaw": 85, "Hand": 0.35
    }

    L = {
        "ShoulderPitch": 66.4, "ShoulderRoll": 26.1,
        "ElbowYaw": -106.0, "ElbowRoll": -44.2,
        "WristYaw": 4.6, "Hand": 0.0
    }

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
