from socket import *
import os
import subprocess

directory = 'Files/'

def add_file(filename):
    try:
        with open(f"{directory}{filename}", 'w') as new_file:
            new_file.write('')
        return f"File '{filename}' created successfully."
    except Exception as e:
        return f"Error creating file '{filename}': {str(e)}"


def remove_file(filename):
    try:
        os.remove(f"{directory}{filename}")
        return f"File '{filename}' removed successfully."
    except Exception as e:
        return f"Error removing file '{filename}': {str(e)}"


def execute_file(filename):
    try:
        full_path = f"{directory}{filename}"
        if filename.endswith('.py'):  # Checking if the file is a Python script
            result = subprocess.run(['python', full_path], capture_output=True, text=True, check=True)
        elif filename.endswith('.js'):  # Checking if the file is a Python script
            result = subprocess.run(['node', full_path], capture_output=True, text=True, check=True)
        else:
            result = subprocess.run([full_path], capture_output=True, text=True, check=True)

        output = result.stdout
        if result.returncode != 0:
            return f"Execution failed for '{filename}'. Error: {result.stderr}"
        return f"Execution of '{filename}' successful. Output: {output}"
    except Exception as e:
        return f"Execution failed for '{filename}': {str(e)}"


def read_file(filename):
    try:
        with open(f"{directory}{filename}", 'r') as file:
            file_contents = file.read()
            return f"Contents of '{filename}':\n{file_contents}"
    except FileNotFoundError:
        return f"File '{filename}' not found."
    except Exception as e:
        return f"Error reading file '{filename}': {str(e)}"


def edit_file(filename, text):
    try:
        if admin:
            with open(f"{directory}{filename}", 'a') as file:
                file.write(f"\n{text}")
            return f"Text added to '{filename}' successfully."
        else:
            return "Only admin can edit files."
    except Exception as e:
        return f"Error editing file '{filename}': {str(e)}"


def clear_file(filename):
    try:
        if admin:
            with open(f"{directory}{filename}", 'w') as file:
                file.write('')
            return f"Content of '{filename}' cleared successfully."
        else:
            return "Only admin can clear files."
    except Exception as e:
        return f"Error erasing file '{filename}': {str(e)}"


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


serverSocket = socket(AF_INET, SOCK_DGRAM)
serverPort = 4445
BUFFER_SIZE = 2048
clients = []
admin = None

serverSocket.bind(("", serverPort))
print("Server is ready to accept requests from clients.")

while True:
    message, clientAddress = serverSocket.recvfrom(BUFFER_SIZE)
    decoded_message = message.decode()
    command_parts = decoded_message.split()

    if clientAddress not in clients:
        clients.append(clientAddress)
        print(clients)
        if admin is None:
            admin = clientAddress
            print(f"{clientAddress} is now the admin.")

    if clientAddress == admin:
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
        elif command_parts[0] == "add" or command_parts[0] == "remove" or command_parts[0] == "execute" or command_parts[0] == "edit" or command_parts[0] == "clear":
            response = "You are not authorized to perform this action."
        else:
            response = "Invalid command."

    serverSocket.sendto(response.encode(), clientAddress)
