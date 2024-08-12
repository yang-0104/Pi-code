import RPi.GPIO as gpio
from picamera import PiCamera     #树莓派摄像头库
# import time            #延时控制
import socket       #通信库
import os
import sys
import struct
from time import sleep


camera = PiCamera()
camera.start_preview()
sleep(5)
filePath = '/home/pi/Y10/image.jpg'
camera.capture(filePath)
camera.stop_preview()
# socket connection
def sock_client(filepath):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('123.56.20.13',2222))
#         s.connect(('192.168.137.113',2222))
        print("success")
    except socket.error as msg:
        print('a')
        print(msg)
        print(sys.exit(1))
    

    while True:
        fhead = struct.pack(b'128sq', bytes(os.path.basename(filepath), encoding='utf-8'), os.stat(filepath).st_size)
        s.send(fhead)
        print('client filepath: {0}'.format(filepath))

        fp = open(filepath, 'rb')
        while 1:
            data = fp.read(1024)
            if not data:
                print('{0} file send over...'.format(filepath))
                break
            s.send(data)
        s.close()
        break

def receiveSize():
    return "size"

def sendString():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('123.56.20.13',2222))
        print("success")
    except socket.error as msg:
        print('a')
        print(msg)
        print(sys.exit(1))
    str = receiveSize().encode("utf-8")
    s.send(str)
    print(str)
    s.close()

def receiveName():
    return "1"

def sendName():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('123.56.20.13',2222))
        print("success")
    except socket.error as msg:
        print('a')
        print(msg)
        print(sys.exit(1))
    str = receiveName().encode("utf-8")
    s.send(str)
    print(str)
    s.close()

def shot():
    filepath = '/home/pi/Y10/image.jpg'
    final_filepath = '/home/pi/Y10/final_image.jpg'
    sock_client(filepath)
    sleep(1)
    sock_client(final_filepath)
    sleep(1)
    sendName()
    sleep(1)
    sendString()

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
    sleep(angle / 360)
    pwmPUL.ChangeDutyCycle(0)

def connectAPP():
    #套接字接口
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #设置IP和端口
    host = '192.168.137.61'
    port = 6666
    #bind绑定该端口
    mySocket.bind((host, port))
    mySocket.listen(10) 
    conn,addr=mySocket.accept()  #等待连接
    print("A")
    msg = "Welcome to Pi server!"
    conn.send(msg.encode()) # send message
    name = conn.recv(1024).decode()
    print(name)
    username = "username: "+name
    conn.send(username.encode())
    while True:
        data = conn.recv(1024)  #接受数据
        data = data.decode()  #解码
        print(data)
        
        if data == "up":
            DIR = 12
            PUL = 18
            gpio.setmode(gpio.BOARD)
            gpio.setup([PUL, DIR], gpio.OUT)
            pwmPUL = gpio.PWM(PUL,600)  
            pwmPUL.start(0)
            sleep(4)
            rotate(1600, "cw")
            pwmPUL.stop()
            gpio.cleanup()
            print("set up")
        if data == "down":
            DIR = 12
            PUL = 18
            gpio.setmode(gpio.BOARD)
            gpio.setup([PUL, DIR], gpio.OUT)
            pwmPUL = gpio.PWM(PUL,600)  
            pwmPUL.start(0)
            sleep(4)
            rotate(1600, "ccw")
            pwmPUL.stop()
            gpio.cleanup()
            print("set up")
            print("set down")
        

        if data == 'show':
            
#             shot()
            f=open ("/home/pi/Y10/final_image.jpg", "rb")
            l = f.read(1024)
            while (l):
                conn.send(l)
                l = f.read(1024)
            print("b")
            print('break down')
            shot()
        
            conn.close()
#             mySocket.close()
            exit()
#         
# if __name__ == '__main__':
while True:
    connectAPP()
#     shot()