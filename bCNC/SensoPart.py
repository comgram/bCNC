import socket

class SensoPart:
    def __init__(self):
        self.HOST = '192.168.100.100'
        self.RPORT = 2005
        self.TPORT = 2006
        self.sr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sr.connect((self.HOST, self.RPORT))
        self.st = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.st.connect((self.HOST, self.TPORT))

    def receive(self):
        # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #     s.connect((self.HOST, self.RPORT))
        #     data = s.recv(1024)
        # s.close()
        self.sr.sendall(bytes("get", 'utf-8'))
        # data = data.decode('utf-8')
        data = bytes()
        start = False
        while True:
            r = self.sr.recv(1)
            if start:
                data += r
                if r == b'>':
                    break
            else:
                if r == b'<':
                    data += r
                    start = True
        # print(data)

        return data

    def receive_my_xd(self):
        # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #     s.connect((self.HOST, self.RPORT))
        #     data = s.recv(1024)
        # s.close()
        self.sr.sendall(bytes("get", 'utf-8'))
        data = self.sr.recv(1024)
        data = data.decode('utf-8')
        temp = data[1:-2].split("|")
        y_d = int(temp[0])
        x_d = int(temp[1])
        # print(y_d, x_d)
        return y_d

    def receive_my_yd(self):
        # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #     s.connect((self.HOST, self.RPORT))
        #     data = s.recv(1024)
        # s.close()
        self.sr.sendall(bytes("get", 'utf-8'))
        data = self.sr.recv(1024)
        data = data.decode('utf-8')
        temp = data[1:-2].split("|")
        y_d = int(temp[0])
        x_d = int(temp[1])
        # print(y_d, x_d)
        return x_d


    def trans(self, cmd):
        # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #     s.connect((self.HOST, self.RPORT))
        #     s.sendall(bytes(cmd, 'utf-8'))
        #     data = s.recv(1024)
        # s.close()
        self.st.sendall(bytes(cmd, 'utf-8'))
        data = self.st.recv(1024)
        return data

    def close(self):
        self.sr.close()
        self.st.close()

    
import time
a = SensoPart()
a.trans('CJB005')
time.sleep(3)
xds = []
yds = []

for i in range(30):
    data = a.receive()
    data = data.decode('utf-8')
    print(data)
    temp = data[1:-2].split("|")
    xd, yd = int(temp[1]), int(temp[0])
    print("{}, {}".format(xd,yd))
    xds.append(xd)
    yds.append(yd)

print("avg xd={}, avg yd={}".format(sum(xds)/30, sum(yds)/30))

xm = round(xd * 0.01 / 46, 3)
ym = round(yd * 0.01 / 424, 3)
print(xm, ym)
a.trans('CJB001')
a.close()