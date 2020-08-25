import socket
import threading

server_name = input("What should your chatroom be called? ")

IP = '0.0.0.0'
PORT = 8000
MSG_SIZE = 2048

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP, PORT))
s.listen(10)
print("Listening for connections...")

clients = []

def new_client():
    while True:
        clientsocket, address = s.accept()

        client_usern = clientsocket.recv(MSG_SIZE)
        client_usern = client_usern.decode("utf-8")

        for client in clients:
            if client[0] == client_usern:
                clientsocket.send(bytes("ERROR: Username already taken!", "utf-8"))
                continue

        client_data = (client_usern, clientsocket)
        clients.append(client_data)

        print(f"Connection from {address} has been established! Username = {client_usern}")
        clientsocket.send(bytes(f"You have joined {server_name} Chatroom.", "utf-8"))

        listen_for_messages_thread = threading.Thread(
            target=listen_for_messages,
            args=(client_data,)
        )

        listen_for_messages_thread.start()


def listen_for_messages(cd):
    while True:
        if len(clients) > 0:
            msg = cd[1].recv(MSG_SIZE)
            msg = msg.decode("utf-8")

            if msg == "[EXIT]":
                cd[1].close()
                clients.remove(cd)

                msg = f"{cd[0]} has left the chat..."

            else:
                msg = f"{cd[0]}: {msg}"

            print(msg)

            msg = msg.encode("utf-8")
            for client in clients:
                client[1].send(msg)


def main():
    new_clients_thread = threading.Thread(target=new_client)
    new_clients_thread.start()


if __name__ == "__main__":
    main()
