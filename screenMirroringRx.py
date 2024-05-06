import socket
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageQt
import sys
import io

<<<<<<< HEAD
def receive_screen(ip, port):
    app = QApplication(sys.argv)
    window = QMainWindow()  # Create a main window
    window.setWindowTitle('Screen Mirroring')
    label = QLabel(window)  # Set label on the window
    window.setCentralWidget(label)
    window.showMaximized()  # Maximize the window to show the entire screen
=======
#private ip address, port
receiver = StreamingServer('172.20.10.6', 9999)
>>>>>>> aeba35034ef4593a05d70268369d36723c0c8460

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))

        while True:
            try:
                # Receive the size of the screenshot
                size_bytes = s.recv(4)
                if not size_bytes:
                    print("Connection closed")
                    break
                size = int.from_bytes(size_bytes, 'big')
                # Collect the entire screenshot data
                img_data = b''
                while len(img_data) < size:
                    packet = s.recv(size - len(img_data))
                    if not packet:
                        break
                    img_data += packet
                if not img_data:
                    break
                img = Image.open(io.BytesIO(img_data))
                pix = ImageQt.toqpixmap(img)
                label.setPixmap(pix)
            except Exception as e:
                print(f"Error occurred: {e}")
            QApplication.processEvents()

    sys.exit(app.exec_())  # Ensure the application runs its event loop

# Replace 'localhost' with the sender's IP address and use the same port
receive_screen('192.168.1.63', 5000)


