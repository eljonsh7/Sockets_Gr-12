from socket import *
import os

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverName = "localhost"  # Replace with your server's hostname or IP address
serverPort = 4444
BUFFER_SIZE = 2048
FILES_DIRECTORY = "Files/"

serverSocket.bind((serverName, serverPort))
print("Server is ready to accept requests from clients.")

clients = {}
admin = None

while True:
    message, clientAddress = serverSocket.recvfrom(BUFFER_SIZE)
    decoded_message = message.decode()

    if clientAddress not in clients:
        clients[clientAddress] = decoded_message
        print(clients)
        if admin is None:
            admin = clientAddress
            print(f"{clientAddress} is now the admin.")
    else:
        if decoded_message.startswith('/command '):
            command = decoded_message.split('/command ')[1]

            if clientAddress == admin:
                # Admin can run any command
                os.chdir(FILES_DIRECTORY)
                output = os.popen(command).read()
                serverSocket.sendto(output.encode(), clientAddress)
                print(f"Admin {clientAddress[0]} executed command: {command}")
            else:
                # Others have read permissions only
                if command.strip() == 'ls':
                    os.chdir(FILES_DIRECTORY)
                    output = os.popen('ls').read()
                    serverSocket.sendto(output.encode(), clientAddress)
                    print(f"User {clientAddress[0]} listed files.")
                else:
                    serverSocket.sendto("Permission denied.".encode(), clientAddress)
                    print(f"User {clientAddress[0]} attempted an unauthorized command.")
        else:
            for address, name in clients.items():
                modified_message = f"{clientAddress[0]}: {decoded_message}"
                serverSocket.sendto(modified_message.encode(), address)
                print(f"{clientAddress[0]}: {decoded_message}")

serverSocket.close()
