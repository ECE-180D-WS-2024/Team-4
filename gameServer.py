import socket
import time
from _thread import *
import sys

server = "172.30.51.245"
port = 5555
currentPlayer = 0

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))
    sys.exit()

s.listen(2)
print("Waiting for a connection, Server Started")

#def get_keypress():
#    keys = event.getKeys()
#    if keys and keys[0] == 'Esc':
#        print("Exiting...")
#        exit()
#    elif keys:
#        return keys[0]
#    else:
#        return None

#Helper Funcitons
def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1]), int(str[2]), int(str[3]), int(str[4]), int(str[5]), int(str[6]), int(str[7]), int(str[8]), int(str[9]), int(str[10])
def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1]) + "," + str(tup[2]) + "," + str(tup[3]) + "," + str(tup[4]) + "," +  str(tup[5]) + "," + str(tup[6]) + "," + str(tup[7]) + "," +  str(tup[8]) + "," + str(tup[9]) + "," + str(tup[10])

players = [(0,0,0,0 , 0,0,0,0 , 0, 0, 0), (0,0,0,0 , 0,0,0,0 , 0, 0, 0)]

def threaded_client(conn, currentP):
    conn.send(str.encode(make_pos(players[currentP])))
    reply = ""
    while True:
        try:
            data = read_pos(conn.recv(2048).decode())
            #reply = data.decode("utf-8")

            players[currentP] = data

            if not data:
                print("Disconnected")
                break
            else:
                if currentP== 1:
                    reply = players[0]
                else:
                    reply = players[1]
                #print("Received: ", data)
                #print("Sending : ", reply)

            conn.sendall(str.encode(make_pos(reply)))
        except:
            break

    print("Lost connection")
    global currentPlayer
    if(currentPlayer != 0):
        currentPlayer -= 1
    conn.close()



while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
#    get_keypress()


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
    