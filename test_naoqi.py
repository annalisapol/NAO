'''
run with .\python2 test_naoqi.py
'''

import sys
sys.path.append("C:\pynaoqi\pynaoqi-python2.7-2.8.6.23-win64-vs2015-20191127_152649\lib")

from naoqi import ALProxy

ip = "127.0.0.1"  
port = 9559

bm = ALProxy("ALBehaviorManager", ip, port)

print("Available behaviors:")
print(bm.getInstalledBehaviors())

bm.runBehavior("StandInit")
