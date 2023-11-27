import socket
import threading
import tkinter as tk
from tkinter import filedialog
sock = None

def receive(sock, signal):
    while signal:
        try:
            data = sock.recv(1024)
            print(str(data.decode("utf-8")))
        except:
            print("You have been disconnected from the server")
            signal = False
            break

def send_file(sock, filename):
    try:
        with open(filename, "rb") as file:
            file_data = file.read(1024)
            while file_data:
                sock.send(file_data)
                file_data = file.read(1024)
            print(f"File '{filename}' sent successfully")
    except Exception as e:
        print(f"Failed to send file '{filename}': {e}")

def choose_file():
    file_path = filedialog.askopenfilename()
    entry_file.delete(0, tk.END)
    entry_file.insert(tk.END, file_path)

def connect_to_server():
    global sock
    global receiveThread

    host = entry_host.get()
    port = int(entry_port.get())

    # Attempt connection to the server
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
    except Exception as e:
        print(f"Could not make a connection to the server: {e}")
        return

    receiveThread = threading.Thread(target=receive, args=(sock, True))
    receiveThread.start()

def send_message():
    global sock
    message = entry_message.get()
    sock.sendall(str.encode(message))

def send_file_to_server():
    global sock
    filename = entry_file.get()
    send_file(sock, filename)

# Create GUI
root = tk.Tk()
root.title("Client Configuration")

root.geometry("500x400")  # Set initial window size

frame = tk.Frame(root)
frame.pack(pady=20)

label_host = tk.Label(frame, text="Enter Host:")
label_host.pack()

entry_host = tk.Entry(frame)
entry_host.pack()

label_port = tk.Label(frame, text="Enter Port:")
label_port.pack()

entry_port = tk.Entry(frame)
entry_port.pack()

connect_button = tk.Button(frame, text="Connect", command=connect_to_server)
connect_button.pack()

message_frame = tk.Frame(root)
message_frame.pack(pady=20)

label_message = tk.Label(message_frame, text="Message:")
label_message.pack()

entry_message = tk.Entry(message_frame)
entry_message.pack()

send_message_button = tk.Button(message_frame, text="Send Message", command=send_message)
send_message_button.pack()

file_frame = tk.Frame(root)
file_frame.pack(pady=20)

label_file = tk.Label(file_frame, text="Select File:")
label_file.pack()

entry_file = tk.Entry(file_frame)
entry_file.pack(side=tk.LEFT, padx=10)

choose_file_button = tk.Button(file_frame, text="Choose File", command=choose_file)
choose_file_button.pack(side=tk.LEFT, padx=10)

send_file_button = tk.Button(file_frame, text="Send File", command=send_file_to_server)
send_file_button.pack(side=tk.LEFT, padx=10)

root.mainloop()
