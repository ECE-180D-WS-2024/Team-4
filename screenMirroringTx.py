#https://www.youtube.com/watch?v=8xy4JKvqsV4
from vidstream import ScreenShareClient
import threading

#private ip address, port
sender = ScreenShareClient('172.20.10.6', 9999)

t = threading.Thread(target= sender.start_stream())
t.start()

while input("") != 'STOP':
    continue

sender.stop_stream()