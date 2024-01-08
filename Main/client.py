from socket import *
import threading


def receive_messages(client_socket):
    while True:
        modified_message = client_socket.recv(BUFFER_SIZE)
        print(modified_message.decode())


clientSocket = socket(AF_INET, SOCK_DGRAM)
serverName = "192.168.151.15"
serverPort = 3500
BUFFER_SIZE = 2048

clientSocket.connect((serverName, serverPort))

receive_thread = threading.Thread(target=receive_messages, args=(clientSocket,))
receive_thread.start()

while True:
    message = input()
    if message.lower() == 'exit':
        break
    clientSocket.send(message.encode())

clientSocket.close()
print("Kjo ip nuk eshte me aktive")