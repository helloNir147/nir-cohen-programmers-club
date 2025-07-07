import socket
import pyautogui
from vidstream import ScreenShareClient
import threading

# הגדרת הלקוח
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.1.146', 12345))

# שיתוף מסך
sender = ScreenShareClient('192.168.1.146', 9999)
t = threading.Thread(target=sender.start_stream)
t.start()

def handle_event(event):
    try:
        event_type, event_info = event.split(":", 1)
    except ValueError:
        print(f"Malformed event: {event}")
        return
    
    try:
        if event_type == "move":
            x, y = map(int, event_info.split(","))
            pyautogui.moveTo(x, y)
        elif event_type == "click":
            x, y, button, pressed = event_info.split(",")
            x, y = int(x), int(y)
            if pressed == "True":
                pyautogui.mouseDown(x, y)
            else:
                pyautogui.mouseUp(x, y)
        elif event_type == "scroll":
            x, y, dx, dy = map(int, event_info.split(","))
            pyautogui.scroll(dy, x=x, y=y)
        elif event_type.startswith("key"):
            key = event_info.replace("'", "")
            if event_type == "key_press":
                pyautogui.keyDown(key)
            elif event_type == "key_release":
                pyautogui.keyUp(key)
    except ValueError as ve:
        print(f"Error processing event: {ve}, event data: {event_info}")

# קבלת וטיפול באירועים
try:
    while True:
        event = client_socket.recv(1024).decode()
        if event:
            handle_event(event)
finally:
    while input("Enter 'STOP' to stop: ") != 'STOP':
        continue
    sender.stop_stream()
    client_socket.close()
