"""
file:01_A_higher_com_service(can_send_cmd).py
socket service
"""

import socket
import sys
import cv2
import numpy

host = "127.0.0.1"  # 服务器ip
port = 2000  # 服务器端口号

# 视频流格式
ip_camera_url = 'http://pi:czc021110@59.110.44.246:5769/'
#ip_camera_url = 'http://pi:czc021110@192.168.137.41:8081/'（局域网内访问）

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
        # while True:
        # data = conn.recv(1024)
        # print('{0} client send data is >>>{1}'.format(address,data.decode()))
        # option(data,conn)
        # if int(data.decode()) > 100:
        #     conn.send(('---> open door!').encode())#cmd1
        # if int(data.decode()) <= 100:
        #     conn.send(('---> close door!').encode())#cmd2
        # if data.decode() == 'capture' :

        # if data == 'exit' or not data:
        #     break
        conn.close()


def option(conn, address):
    while True:
        data = conn.recv(1024)
        print('{0} client send data is >>>{1}'.format(address, data.decode()))
#         if int(data.decode()) > 100:
#            conn.send(('---> open door!').encode())  # cmd1
#         if int(data.decode()) <= 100:
#            conn.send(('---> close door!').encode())  # cmd2
        if data.decode() == 'cap':
            print('now starting to send video...')
            conn.send(('ok').encode())  # cmd3    
        if data == 'exit' or not data:
            break


if __name__ == '__main__':
    socket_service()