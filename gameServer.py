import socket
import time
from _thread import *
import sys

server = "172.16.1.36"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")


def threaded_client(conn,):
    conn.send(str.encode("Connected"))
    reply = ""
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode("utf-8")

            if not data:
                print("Disconnected")
                break
            else:
                print("Received: ", reply)
                print("Sending : ", reply)

            conn.sendall(str.encode(reply))
        except:
            break

    print("Lost connection")
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn,))


#######################################
#CREATION OF NETWORK SOCKET AFTER THE START SCREEN
#from gameNetwork import *
#player1client = Network()

#Helper Funcitons
#def read_pos(str):
#    str = str.split(",")
#    return int(str[0]), int(str[1]), bool(str[2])

#def make_pos(tup):
#    return str(tup[0]) + "," + str(tup[1]) + "," + str(tup[2])

#######################################
    


