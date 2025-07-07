import socket
import os

def send_all(sock, data):
    sock.sendall(data)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 9998))

file_path = r"C:\Users\User\Desktop\fgf.txt"
file_name = "received_image.txt"
file_size = os.path.getsize(file_path)

# Send file name length and file name
file_name_encoded = file_name.encode()
file_name_length = len(file_name_encoded)
client.send(f"{file_name_length:04}".encode())  # Send fixed 4-byte length
client.send(file_name_encoded)

# Send file size
client.send(f"{file_size:08}".encode())  # Send fixed 8-byte size

# Send file data
with open(file_path, "rb") as file:
    while chunk := file.read(1024):
        send_all(client, chunk)

client.close()
print("File sent successfully!")
