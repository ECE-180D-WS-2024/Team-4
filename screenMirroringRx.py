#https://www.youtube.com/watch?v=8xy4JKvqsV4
from vidstream import StreamingServer
import threading

#private ip address, port
receiver = StreamingServer('127.0.0.1', 9999)


t = threading.Thread(target= receiver.start_server)
t.start()

while input("") != 'STOP':
    continue

receiver.stop_server()
