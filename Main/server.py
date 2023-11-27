import socket
import threading
import tkinter as tk

# Variables for holding information about connections
connections = []
total_connections = 0
connection_list = None  # Define connection_list globally
entry_host = None  # Define entry_host globally
entry_port = None  # Define entry_port globally

# Client class, new instance created for each connected client
# Each instance has the socket and address that is associated with items
# Along with an assigned ID and a name chosen by the client
class Client(threading.Thread):
    def __init__(self, socket, address, id, name, signal):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = id
        self.name = name
        self.signal = signal

    def __str__(self):
        return str(self.id) + " " + str(self.address)

    # Attempt to get data from client
    # If unable to, assume client has disconnected and remove him from server data
    # If able to and we get data back, print it in the server and send it back to every
    # client aside from the client that has sent it
    # .decode is used to convert the byte data into a printable string
    def run(self):
        while self.signal:
            try:
                data = self.socket.recv(32)
            except:
                print("Client " + str(self.address) + " has disconnected")
                self.signal = False
                connections.remove(self)
                break
            if data != "":
                print("ID " + str(self.id) + ": " + str(data.decode("utf-8")))
                for client in connections:
                    if client.id != self.id:
                        client.socket.sendall(data)

# Wait for new connections
def new_connections(socket):
    while True:
        sock, address = socket.accept()
        global total_connections
        connections.append(Client(sock, address, total_connections, "Name", True))
        connections[len(connections) - 1].start()
        print("New connection at ID " + str(connections[len(connections) - 1]))
        total_connections += 1

def start_server():
    global host, port
    host = entry_host.get()
    port = int(entry_port.get())

    # Create new server socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(5)

    # Create new thread to wait for connections
    new_connections_thread = threading.Thread(target=new_connections, args=(sock,))
    new_connections_thread.start()

def update_connections():
    global connection_list  # Access connection_list from the global scope
    connection_list.delete(0, tk.END)
    for connection in connections:
        connection_list.insert(tk.END, str(connection))

def update_gui_connections():
    while True:
        update_connections()
        connection_list.after(1000, update_gui_connections)
        break

def main():
    global host, port, connection_list, entry_host, entry_port  # Declare variables as global
    host = ""
    port = 0

    root = tk.Tk()
    root.title("Server Configuration")

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

    start_button = tk.Button(frame, text="Start Server", command=start_server)
    start_button.pack()

    connection_frame = tk.Frame(root)
    connection_frame.pack(pady=20)

    connection_label = tk.Label(connection_frame, text="Connections:")
    connection_label.pack()

    connection_list = tk.Listbox(connection_frame, width=50, height=15)
    connection_list.pack()

    update_gui_connections()

    root.mainloop()

if __name__ == "__main__":
    main()
