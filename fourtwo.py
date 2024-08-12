import RPi.GPIO as gpio
import time

DIR = 12
PUL = 18

gpio.setmode(gpio.BOARD)
gpio.setup([PUL, DIR], gpio.OUT)

# 别问我这里为什么是2085不是1600，我也很纳闷，试了很久，发现这个频率才刚好转够一圈 > . <
pwmPUL = gpio.PWM(PUL,600)  
pwmPUL.start(0)

def rotate(angle, direction):
    """
    旋转操作，需要指定旋转角度和方向
    :param angle: 正整型数据，旋转角度
    :param direction: 字符串数据，旋转方向，取值为："ccw"或"cw".ccw:逆时针旋转，cw:顺时针旋转
    :ccw:qian
    :cw:hou
    :return:None
    """
    if direction == "ccw":
        gpio.output(DIR, gpio.LOW)
    elif direction == "cw":
        gpio.output(DIR, gpio.HIGH)
    else:
        return
    pwmPUL.ChangeDutyCycle(50)
    time.sleep(angle / 360)
    pwmPUL.ChangeDutyCycle(0)

time.sleep(5)
rotate(1600, "cw")
time.sleep(2)
rotate(1400, "ccw")


pwmPUL.stop()
gpio.cleanup()
print('ok')