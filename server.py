import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 8000))
s.listen(10)
print("Listening for connections...")

clients = []

while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")
    clientsocket.send(bytes("You have joined MysteryCoder456 Chatroom.", "utf-8"))
    clients.append(clientsocket)
