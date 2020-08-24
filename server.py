import socket
import threading

IP = '127.0.0.1'
PORT = 8000
MSG_SIZE = 2048

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP, PORT))
s.listen(10)
print("Listening for connections...")

clients = {}

def new_client():
    while True:
        clientsocket, address = s.accept()

        client_usern = clientsocket.recv(MSG_SIZE)
        client_usern = client_usern.decode("utf-8")

        if client_usern in clients.keys():
            clientsocket.send(bytes("ERROR: Username already taken!", "utf-8"))
        else:
            clients[client_usern] = clientsocket

            print(f"Connection from {address} has been established! Username = {client_usern}")
            clientsocket.send(bytes("You have joined MysteryCoder456 Chatroom.", "utf-8"))
            listen_for_messages_thread = threading.Thread(
                target=listen_for_messages,
                args=(clients[client_usern],)
            )
            listen_for_messages_thread.start()


def listen_for_messages(cs: socket.socket):
    while True:
        if len(clients) > 0:
            msg = cs.recv(MSG_SIZE)
            msg = msg.decode("utf-8")
            print(msg)


def main():
    new_clients_thread = threading.Thread(target=new_client)
    new_clients_thread.start()


if __name__ == "__main__":
    main()
