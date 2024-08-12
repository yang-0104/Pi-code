"""
file:01_A_higher_com_service(can_send_cmd).py
socket service
"""

import time
import socket
import sys
import cv2
import numpy

host = "127.0.0.1"  # 服务器本地ip
port = 2000  # 服务器端口号


def socket_service():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 防止socket server重启后端口被占用（socket.error: [Errno 98] Address already in use）
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #打开地址复用功能
        s.bind((host, port))
        s.listen(10)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    #print('Waiting connection...')
    print('等待连接...')

    while True:
        conn, address = s.accept()
        #print('Accept new connection from {0}'.format(address))
        print('连接IP %s 成功' % address[0])
        #conn.send(('Hi, Welcome to the server!').encode())#encode是编码函数（utf-8）
        conn.send(('您已成功连接树莓派！').encode())
        option(conn, address)
        #接受客户端指令
        conn.close()


def lift(direction):
    import RPi.GPIO as gpio
    DIR = 12
    PUL = 18

    gpio.setmode(gpio.BOARD)
    gpio.setup([PUL, DIR], gpio.OUT)

    # 别问我这里为什么是2085不是1600，我也很纳闷，试了很久，发现这个频率才刚好转够一圈 > . <
    pwmPUL = gpio.PWM(PUL, 2085)
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
        if direction == "down":
            gpio.output(DIR, gpio.LOW)
        elif direction == "up":
            gpio.output(DIR, gpio.HIGH)
        else:
            return
        pwmPUL.ChangeDutyCycle(50)
        #控制转速
        time.sleep(angle / 360)
        pwmPUL.ChangeDutyCycle(0)

    time.sleep(1)
    rotate(1800, direction)
    pwmPUL.stop()
    gpio.cleanup()
    print('ok')



def option(conn, address):
    while True:
        data = (conn.recv(1024)).decode()
        print('{0} client send data is >>>{1}'.format(address, data))
        if data == 'cap':#cmd1
            print('now starting to send video...')
            conn.send(('视频流已经发送').encode())
        if data =='up':
            lift('up')
            conn.send(('平台已经上升x厘米').encode())
        if data =='down':
            lift('down')
            conn.send(('平台已经下降x厘米').encode())
        if data == 'exit' or not data:
            break


if __name__ == '__main__':
    socket_service()