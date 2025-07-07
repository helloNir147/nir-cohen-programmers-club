import socket
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
from vidstream import StreamingServer
import threading

# הגדרת השרת
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('192.168.1.146', 12345))
server_socket.listen(1)
print("Waiting for connection...")
client_socket, client_address = server_socket.accept()
print(f"Connected to {client_address}")

def send_event(event):
    try:
        client_socket.sendall(event.encode())
    except ConnectionResetError:
        print("החיבור הופסק על ידי הלקוח.")
    except Exception as e:
        print(f"התרחשה שגיאה: {e}")

# הגדרות מסך
receiver = StreamingServer('192.168.1.146', 9999)
t = threading.Thread(target=receiver.start_server)
t.start()

# מאזין לעכבר
def on_move(x, y):
    send_event(f"move:{x},{y}")

def on_click(x, y, button, pressed):
    send_event(f"click:{x},{y},{button},{pressed}")

def on_scroll(x, y, dx, dy):
    send_event(f"scroll:{x},{y},{dx},{dy}")

# מאזין למקלדת
def on_press(key):
    send_event(f"key_press:{key}")

def on_release(key):
    send_event(f"key_release:{key}")

mouse_listener = MouseListener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
keyboard_listener = KeyboardListener(on_press=on_press, on_release=on_release)

mouse_listener.start()
keyboard_listener.start()

# שמירה על השרת פעיל
try:
    mouse_listener.join()
    keyboard_listener.join()
    while True:
        if input() == "STOP":
            break
finally:
    receiver.stop_server()
    client_socket.close()
    server_socket.close()
