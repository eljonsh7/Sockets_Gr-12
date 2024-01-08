from socket import *
import os
import subprocess
import shutil

directory = 'Files/'


def add_file(file):
    try:
        with open(f"{directory}{file}", 'w') as new_file:
            new_file.write('')
        return f"File '{file}' created successfully."
    except Exception as e:
        return f"Error creating file '{file}': {str(e)}"


def remove_file(file):
    try:
        os.remove(f"{directory}{file}")
        return f"File '{file}' removed successfully."
    except Exception as e:
        return f"Error removing file '{file}': {str(e)}"


def execute_file(file):
    try:
        full_path = f"{directory}{file}"
        if file.endswith('.py'):  # Checking if the file is a Python script
            result = subprocess.run(['python', full_path], capture_output=True, text=True, check=True)
        elif file.endswith('.js'):  # Checking if the file is a Python script
            result = subprocess.run(['node', full_path], capture_output=True, text=True, check=True)
        else:
            result = subprocess.run([full_path], capture_output=True, text=True, check=True)

        output = result.stdout
        if result.returncode != 0:
            return f"Execution failed for '{file}'. Error: {result.stderr}"
        return f"Execution of '{file}' successful. Output: {output}"
    except Exception as e:
        return f"Execution failed for '{file}': {str(e)}"


def read_file(file):
    f = file
    try:
        with open(f"{directory}{file}", 'r') as file:
            file_contents = file.read()
            return f"Contents of '{f}':\n{file_contents}"
    except FileNotFoundError:
        return f"File '{file}' not found."
    except Exception as e:
        return f"Error reading file '{file}': {str(e)}"


def edit_file(file, txt):
    f = file
    try:
        if admin:
            with open(f"{directory}{file}", 'a') as file:
                file.write(f"\n{txt}")
            return f"Text added to '{f}' successfully."
        else:
            return "Only admin can edit files."
    except Exception as e:
        return f"Error editing file '{f}': {str(e)}"


def clear_file(file):
    f = file
    try:
        if admin:
            with open(f"{directory}{file}", 'w') as file:
                file.write('')
            return f"Content of '{f}' cleared successfully."
        else:
            return "Only admin can clear files."
    except Exception as e:
        return f"Error erasing file '{f}': {str(e)}"


def list_files():
    try:
        files = os.listdir(directory)
        files_list = "\n".join(files)
        return f"Files in directory:\n{files_list}"
    except Exception as e:
        return f"Error listing files: {str(e)}"


def make_directory(dirname):
    try:
        if admin:
            os.mkdir(f"{directory}{dirname}")
            return f"Directory '{dirname}' created successfully."
        else:
            return "Only admin can create directories."
    except Exception as e:
        return f"Error creating directory '{dirname}': {str(e)}"


def change_directory(dirname):
    try:
        global directory
        if dirname == '..':
            if directory != 'Files/':
                directory = '/'.join(directory.split('/')[:-2]) + '/'
        else:
            if os.path.isdir(f"{directory}{dirname}"):
                directory = f"{directory}{dirname}/"
        return f"Current directory: {directory}"
    except Exception as e:
        return f"Error changing directory: {str(e)}"


def delete_directory(dirname):
    try:
        shutil.rmtree(f"{directory}{dirname}")
        return f"Folder '{dirname}' deleted successfully."
    except Exception as e:
        return f"Error deleting folder '{dirname}': {str(e)}"


serverSocket = socket(AF_INET, SOCK_DGRAM)
serverName = '192.168.151.15'
serverPort = 3500
BUFFER_SIZE = 2048
clients = []
admin = '192.168.151.215'

serverSocket.bind((serverName, serverPort))
print("Server is ready to accept requests from clients.")

while True:
    message, clientAddress = serverSocket.recvfrom(BUFFER_SIZE)
    decoded_message = message.decode()
    command_parts = decoded_message.split()

    if clientAddress not in clients:
        clients.append(clientAddress)
        print(clients)
        if admin is None:
            admin = clientAddress[0]
            print(f"{clientAddress} is now the admin.")

    print(f"{clientAddress}: {decoded_message}.")

    if command_parts[0] == "msg":
        with open(f"commands.txt", 'a') as file:
            file.write(f"\n{clientAddress}: {decoded_message}.")

    if clientAddress[0] == admin:
        if command_parts[0] == "add":
            if len(command_parts) < 2:
                response = "Usage: add <filename>"
            else:
                response = add_file(command_parts[1])
        elif command_parts[0] == "remove":
            if len(command_parts) < 2:
                response = "Usage: remove <filename>"
            else:
                response = remove_file(command_parts[1])
        elif command_parts[0] == "execute":
            if len(command_parts) < 2:
                response = "Usage: execute <filename>"
            else:
                response = execute_file(command_parts[1])
        elif command_parts[0] == "edit":
            if len(command_parts) < 3:
                response = "Usage: edit <filename> <text>"
            else:
                filename = command_parts[1]
                text = ' '.join(command_parts[2:])
                response = edit_file(filename, text)
        elif command_parts[0] == "clear":
            if len(command_parts) < 2:
                response = "Usage: clear <filename>"
            else:
                response = clear_file(command_parts[1])
        elif command_parts[0] == "ls":
            response = list_files()
        elif command_parts[0] == "read":
            if len(command_parts) < 2:
                response = "Usage: read <filename>"
            else:
                response = read_file(command_parts[1])
        elif command_parts[0] == "mkdir":
            if len(command_parts) < 2:
                response = "Usage: mkdir <dirname>"
            else:
                response = make_directory(command_parts[1])
        elif command_parts[0] == "rmdir":
            if len(command_parts) < 2:
                response = "Usage: rmdir <dirname>"
            else:
                response = delete_directory(command_parts[1])
        elif command_parts[0] == "cd":
            if len(command_parts) < 2:
                response = "Usage: cd <dirname or '..'>"
            else:
                response = change_directory(command_parts[1])
        else:
            response = "Invalid command."
    else:
        if command_parts[0] == "read":
            if len(command_parts) < 2:
                response = "Usage: read <filename>"
            else:
                response = read_file(command_parts[1])
        elif command_parts[0] == "ls":
            response = list_files()
        elif command_parts[0] == "cd":
            if len(command_parts) < 2:
                response = "Usage: cd <dirname or '..'>"
            else:
                response = change_directory(command_parts[1])
        elif (command_parts[0] == "add" or command_parts[0] == "remove" or command_parts[0] == "execute" or
              command_parts[0] == "edit" or command_parts[0] == "clear" or command_parts[0] == "mkdir" or
              command_parts[0] == "rmdir"):
            response = "You are not authorized to perform this action."
        else:
            response = "Invalid command."

    serverSocket.sendto(response.encode(), clientAddress)
