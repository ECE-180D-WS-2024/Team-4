import socket


#Helper Funcitons
def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1]), int(str[2]), int(str[3]), bool(str[4]), bool(str[5]), bool(str[6])

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1]) + "," + str(tup[2]) + "," + str(tup[3]) + "," + str(tup[4]) + "," +  str(tup[5]) + "," + str(tup[6])

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "172.30.51.245"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.pos = self.connect()
        #print(self.pos)
        

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)

    def receive(self):
        try:
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)



