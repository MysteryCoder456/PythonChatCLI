import socket

server_name = input("What should your server's name be? ")
max_clients = int(input("What is the maximum number of people your server should have? "))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 8000))
s.listen(max_clients)
print("Listening for connections...")

clients = []

while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")
    clientsocket.send(bytes(f"You have joined {server_name} server.", "utf-8"))
    clients.append(clientsocket)
