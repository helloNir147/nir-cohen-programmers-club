import socket

def receive_all(sock, size):
    data = b''
    while len(data) < size:
        packet = sock.recv(size - len(data))
        if not packet:
            return None
        data += packet
    return data

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 9998))
server.listen(1)
print("Server is listening...")

client, addr = server.accept()
print(f"Connection from {addr}")

# Receiving file name
file_name_length = int(client.recv(4).decode())
file_name = client.recv(file_name_length).decode()
print("File name received:", file_name)

# Receiving file size
file_size = int(client.recv(8).decode())
print("File size received:", file_size)

file = open(file_name, 'wb')
total_received = 0
print("Receiving file...")

while total_received < file_size:
    data = client.recv(1024)
    if not data:
        break
    file.write(data)
    total_received += len(data)
    percent_done = (total_received / file_size) * 100
    print(f"Progress: {percent_done:.2f}%", end='\r')

file.close()
client.close()
server.close()
print("\nFile received successfully!")
