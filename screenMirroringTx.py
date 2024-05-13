from vidstream import ScreenShareClient
import threading

sender = ScreenShareClient('172.16.1.36', 9999)

t = threading.Thread(target=sender.start_stream)
t.start()

while input("") != 'STOP':
    continue

sender.stop_stream()