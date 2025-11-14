# NAO fa 3 passi indietro

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

    # Movement parameters (3 short backward steps)
    distance_x_m = -0.08     # backward
    distance_y_m = 0.0
    theta_deg = 0.0

    # Disable arm movement
    motionProxy.setMoveArmsEnabled(False, False)

    # Execute backward movement
    motionProxy.moveTo(distance_x_m, distance_y_m, theta_deg)

if __name__ == "__main__":

    robotIP = "127.0.0.1"
    port = 9559

    if len(sys.argv) >= 2:
        robotIP = sys.argv[1]
    if len(sys.argv) >= 3:
        port = int(sys.argv[2])

    main(robotIP, port)
