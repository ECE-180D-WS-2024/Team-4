from vidstream import StreamingServer
import threading

receiver = StreamingServer('172.16.1.36', 9999)

t = threading.Thread(target=receiver.start_server)
t.start()

while input("") != 'STOP':
    continue

receiver.stop_server()
#this is a comment

