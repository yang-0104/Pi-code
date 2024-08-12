def receiveSize():
    return "aaaaa"

def sendString():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('123.56.20.13',2223))
        print("success")
    except socket.error as msg:
        print('a')
        print(msg)
        print(sys.exit(1))
    str = receiveSize().encode("utf-8")
    s.send(str)
    print(str)
    s.close()