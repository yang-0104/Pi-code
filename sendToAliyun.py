#import socket
from socket import *
import time


HOST = '公网地址'
PORT = 2222
BUFSIZ = 1024
ADDR = (HOST,PORT)

try:
    mySocket = socket(AF_INET,SOCK_STREAM)
    mySocket.connect(ADDR)
    print("连接到服务器")
except :                           ##连接不成功，运行最初的ip
    print ('连接不成功')
    
while True:
    #发送消息
    msg = '9'
    #编码发送
    mySocket.send(msg.encode("utf-8"))
    print("发送完成")
    
    time.sleep(10)
    
    if msg == "over":
        mySocket.close()
        print("程序结束\n")
        exit()       
print("程序结束\n")



