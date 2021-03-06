import sys
import socket
import threading
import urllib.request

if len(sys.argv) > 1:
    WLCM_MSG = sys.argv[1]
else:
    WLCM_MSG = input("What should your Welcome Message be? ")
WLCM_MSG = WLCM_MSG.encode("utf-8")

ADDR = '0.0.0.0'
PORT = 8000

MSG_SIZE = 2048

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((ADDR, PORT))
s.listen(5)
print("Listening for connections at:")
print("Local IP:", socket.gethostbyname(socket.gethostname()), ", Public IP:", urllib.request.urlopen('https://ident.me').read().decode('utf8'), ", Port:", PORT)

clients = []

def new_client():
    while True:
        clientsocket, address = s.accept()

        client_usern = clientsocket.recv(MSG_SIZE)
        client_usern = client_usern.decode("utf-8")

        usern_taken = False

        for client in clients:
            if client[0] == client_usern:
                clientsocket.send(bytes("ERROR: Username already taken!", "utf-8"))
                usern_taken = True

        if usern_taken:
            continue

        for client in clients:
            client[1].send(bytes(f"{client_usern} has entered the chat...", "utf-8"))

        client_data = (client_usern, clientsocket)
        clients.append(client_data)

        listen_for_messages_thread = threading.Thread(
            target=listen_for_messages,
            args=(client_data,)
        )

        listen_for_messages_thread.start()

        print(f"Connection from {address} has been established! Username = {client_usern}")
        clientsocket.send(WLCM_MSG)


def listen_for_messages(cd):
    has_left = False
    while not has_left:
        if len(clients) > 0:
            msg = cd[1].recv(MSG_SIZE)
            msg = msg.decode("utf-8")

            if msg == "[EXIT]":
                cd[1].close()
                clients.remove(cd)
                has_left = True
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
