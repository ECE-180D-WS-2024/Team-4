import socket
import time
from Quartz import CGWindowListCopyWindowInfo, kCGNullWindowID, kCGWindowListOptionOnScreenOnly, CGWindowListCreateImage, kCGWindowImageBoundsIgnoreFraming, CGRectNull
from Quartz.CoreGraphics import CGRectMake
import Quartz.CoreGraphics as CG
from AppKit import NSBitmapImageRep, NSJPEGFileType
from PIL import Image

def capture_window(title):
    window_list = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, kCGNullWindowID)
    for window in window_list:
        window_name = window.get('kCGWindowName', '')
        if title.lower() in window_name.lower():
            window_id = window['kCGWindowNumber']
            bounds_dict = window['kCGWindowBounds']
            bounds = CGRectMake(bounds_dict['X'], bounds_dict['Y'], bounds_dict['Width'], bounds_dict['Height'])
            image = CGWindowListCreateImage(bounds, kCGWindowListOptionOnScreenOnly, window_id, kCGWindowImageBoundsIgnoreFraming)
            bitmap_rep = NSBitmapImageRep.alloc().initWithCGImage_(image)
            data = bitmap_rep.representationUsingType_properties_(NSJPEGFileType, None)
            return data

def send_screen(ip, port, window_title):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((ip, port))
        s.listen(1)
        print("Waiting for a connection...")
        conn, addr = s.accept()
        print(f"Connected by {addr}")

        try:
            while True:
                image_data = capture_window(window_title)
                if image_data:
                    size = len(image_data)
                    conn.sendall(size.to_bytes(4, 'big'))
                    conn.sendall(image_data)
                else:
                    print("No window found with specified title.")
                time.sleep(1)  # Adjust the frame rate
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()

# Replace 'localhost' with the receiver's IP address, set the port and window title
send_screen('192.168.1.63', 5000, "Super Minigolf")
