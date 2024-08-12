import RPi.GPIO as GPIO
import time
import sys
from array import *
 
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)
 
steps    = 600 # 步进数
clockwise = 1 # 1=顺时针 0=逆时针
 
print('start')
arr = [0,1,2,3]
if clockwise!=1:
    arr = [3,2,1,0]
 
ports = [17,18,27,22] #使用BCM I/O 如上图所示
 
for p in ports:
    GPIO.setup(p,GPIO.OUT)
    
for x in range(0,steps):
    for j in arr:
        time.sleep(0.01)
        for i in range(0,4):
            if i == j:            
                GPIO.output(ports[i],True)
            else:
                GPIO.output(ports[i],False)
GPIO.cleanup()
print('ok')