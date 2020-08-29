import sys
import socket
import threading

ADDR = input("Enter the server's IP Address/DNS (leave empty for localhost): ")
PORT = input("Enter the server's PORT (leave empty for 8000): ")

if len(ADDR.strip()) < 1:
    ADDR = '127.0.0.1'

if len(PORT.strip()) < 1:
    PORT = 8000
else:
    PORT = int(PORT)

MSG_SIZE = 2048

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect((ADDR, PORT))
except ConnectionRefusedError:
    print("This server has not been started...")
    sys.exit()

usern = input("Enter your username: ")
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
        print("\n" + welcome_msg)
        print("Use [EXIT] to leave this room.\n")


def listen_for_messages():
    while not stop_threads:
        msg = s.recv(MSG_SIZE)
        msg = msg.decode("utf-8")
        print(msg)


def send_messages():
    while not stop_threads:
        msg = input()
        msg = msg.encode("utf-8")
        s.send(msg)

        if msg.decode("utf-8") == "[EXIT]":
            stop_all_threads()


def stop_all_threads():
    global stop_threads
    stop_threads = True


def main():
    contact_server()
    listen_for_messages_thread = threading.Thread(target=listen_for_messages)
    send_messages_thread = threading.Thread(target=send_messages)

    listen_for_messages_thread.start()
    send_messages_thread.start()

    while True:
        try:
            if stop_threads:
                listen_for_messages_thread.join()
                send_messages_thread.join()
                break
        except KeyboardInterrupt:
            stop_all_threads()
            s.send(bytes("[EXIT]", "utf-8"))
            listen_for_messages_thread.join()
            send_messages_thread.join()
            break


if __name__ == "__main__":
    main()
