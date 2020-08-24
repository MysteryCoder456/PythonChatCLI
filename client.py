import sys
import socket
import threading

IP = '34.230.88.196'
PORT = 8000
MSG_SIZE = 2048

usern = input("Enter your username: ")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect((IP, PORT))
except ConnectionRefusedError:
    print("This server has not started yet...")
    sys.exit()


stop_threads = False


def contact_server():
    encoded_usern = usern.encode("utf-8")
    s.send(encoded_usern)

    welcome_msg = s.recv(MSG_SIZE)
    welcome_msg = welcome_msg.decode("utf-8")
    if "ERROR" in welcome_msg:
        print(welcome_msg)
        sys.exit()
    else:
        print(welcome_msg)
        print("Use [EXIT] to leave this room.\n")


def listen_for_messages():
    while True:
        msg = s.recv(MSG_SIZE)
        msg = msg.decode("utf-8")
        print(msg)

        if stop_threads:
            break


def send_messages():
    while True:
        msg = input()
        msg = msg.encode("utf-8")
        s.send(msg)

        if msg.decode("utf-8") == "[EXIT]":
            global stop_threads
            stop_threads = True
            break


def main():
    contact_server()
    listen_for_messages_thread = threading.Thread(target=listen_for_messages)
    send_messages_thread = threading.Thread(target=send_messages)

    listen_for_messages_thread.start()
    send_messages_thread.start()

    while True:
        if stop_threads:
            listen_for_messages_thread.join()
            send_messages_thread.join()
            break


if __name__ == "__main__":
    main()
