from tkinter import *
from tkinter import filedialog
from socket import *
import os

clientSocket = socket(AF_INET, SOCK_DGRAM)
serverName = "127.0.0.1"
serverPort = 4444
BUFFER_SIZE = 2048


def send_message():
    message = message_entry.get()
    clientSocket.sendto(message.encode(), (serverName, serverPort))
    message_entry.delete(0, END)

def add_file():
    file_path = filedialog.askopenfilename()  # Open file dialog to select a file
    if file_path:
        file_name = os.path.basename(file_path)
        clientSocket.sendto(f"ADD_FILE {file_name}".encode(), (serverName, serverPort))
        with open(file_path, "rb") as file:
            file_data = file.read()
            clientSocket.sendto(file_data, (serverName, serverPort))


def delete_file():
    selected_file = file_listbox.get(file_listbox.curselection())
    clientSocket.sendto(f"DELETE_FILE {selected_file}".encode(), (serverName, serverPort))

def download_file():
    selected_file = file_listbox.get(file_listbox.curselection())
    # Implement file download functionality here

def receive_messages():
    while True:
        try:
            message, _ = clientSocket.recvfrom(BUFFER_SIZE)
            if not message:
                break
            decoded_message = message.decode()
            if ":" in decoded_message:
                received_messages.insert(END, decoded_message)
            elif decoded_message.startswith("NEW_FILE"):
                file_name = decoded_message.split()[1]
                file_listbox.insert(END, file_name)
        except OSError as e:
            print(f"Error receiving message: {e}")
            break


def update_file_list():
    clientSocket.sendto("GET_FILES".encode(), (serverName, serverPort))
    # Receive file list from server and update file_listbox
    # Replace this comment with logic to update the file_listbox

# GUI setup
root = Tk()
root.title("Client")

# Part 1: Sending Messages
message_frame = Frame(root)
message_label = Label(message_frame, text="Message:")
message_label.pack(side=LEFT)
message_entry = Entry(message_frame, width=40)
message_entry.pack(side=LEFT)
send_button = Button(message_frame, text="Send", command=send_message)
send_button.pack(side=LEFT)
message_frame.pack(pady=10)

# Part 2: Displaying Received Messages
messages_frame = Frame(root)
messages_label = Label(messages_frame, text="Received Messages:")
messages_label.pack()
received_messages = Listbox(messages_frame, width=60, height=15)
received_messages.pack()
messages_frame.pack(pady=10)

# Part 3: Managing Files
files_frame = Frame(root)
files_label = Label(files_frame, text="Files:")
files_label.pack()
file_listbox = Listbox(files_frame, width=40, height=10)
file_listbox.pack()
add_button = Button(files_frame, text="Add", command=add_file)
add_button.pack(side=LEFT)
delete_button = Button(files_frame, text="Delete", command=delete_file)
delete_button.pack(side=LEFT)
download_button = Button(files_frame, text="Download", command=download_file)
download_button.pack(side=LEFT)
files_frame.pack(pady=10)

import threading
receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True
receive_thread.start()
print(receive_thread)

# Start the GUI
root.mainloop()

clientSocket.close()
