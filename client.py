import socket
import sys

HOST = '192.168.31.104'  # The server's hostname or IP address
PORT = 80        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(bytes(str(sys.argv[1]), encoding="UTF-8"))
    data = s.recv(1024)

print("Done")