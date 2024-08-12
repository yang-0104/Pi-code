import socket  # 通信库
import RPi.GPIO as gpio

from time import sleep


# final_filePath = 'cache3.jpg'
final_filePath = '/home/pi/Y10/final_image.jpg'
# original_filePath = "image3.jpg"
original_filePath = '/home/pi/Y10/image.jpg'

DIR = 12
PUL = 18

gpio.setmode(gpio.BOARD)
gpio.setup([PUL, DIR], gpio.OUT)

pwmPUL = gpio.PWM(PUL, 600)


def connectAPP():
    # 套接字接口
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置IP和端口
    # host = '192.168.31.214'
    host = '192.168.137.42'
    port = 6666
    # bind绑定该端口
    mySocket.bind((host, port))
    mySocket.listen(10)
    print("等待连接")
    conn, addr = mySocket.accept()  # 等待连接
    print("A")

    while True:

        print("已连接")
        data = conn.recv(1024)  # 接受数据
        data = data.decode()  # 解码
        print(data)
        if data == "齿轮":  # 零件类型：齿轮
            print("齿轮")  # 调用齿轮函数
            size = getSize().encode("utf-8")
            print(getSize())
            conn.send(size)
            print("success")
            break

        if data == "up":
            pwmPUL.start(0)
            sleep(3)
            rotate(1600, "cw")
            pwmPUL.stop()
            gpio.cleanup()
            print('ok')
            print("set up")
        #     此处添加控制步进电机，向上运动

        if data == "down":
            pwmPUL.start(0)
            sleep(3)
            rotate(1600, "ccw")
            pwmPUL.stop()
            gpio.cleanup()
            print('ok')
            print("set down")
        #     此处添加控制步进电机，向下运动

        if data == "final_image":
            sendImg(conn, final_filePath)

        if data == 'show':
            sendImg(conn, original_filePath)

        if data == "already":
            break

        if data == "":
            break


def sendImg(conn, filePath):
    # filepath = 'image.jpg'  # 输入需要传输的图片名 xxx.jpg
    print('发送图片线程启动')

    fp = open(filePath, 'rb')  # 打开要传输的图片
    while True:
        data = fp.read(1024)  # 读入图片数据
        if not data:
            print('{0} send over...'.format(filePath))
            break
        conn.send(data)  # 以二进制格式发送图片数据
    sleep(1)


def rotate(angle, direction):
    """
    旋转操作，需要指定旋转角度和方向
    :param angle: 正整型数据，旋转角度
    :param direction: 字符串数据，旋转方向，取值为："ccw"或"cw".ccw:逆时针旋转，cw:顺时针旋转
    :cw:上移
    :ccw:下移
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


def getSize():
    return "0.5105\n19.9106\n1.6038\n17.8146\n20.0524\n39.0\n[13.0555  5.2777][ 1.9444 13.8888][11.1111 8.6111]"


while True:
    connectAPP()