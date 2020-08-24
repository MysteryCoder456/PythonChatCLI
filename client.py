import socket

usern = input("Enter your username: ")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 8000))

while True:
    welcome_msg = s.recv(1024)
    welcome_msg = welcome_msg.decode("utf-8")
    print(welcome_msg)
