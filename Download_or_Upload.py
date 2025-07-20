import socket
import threading
import tkinter as tk
from tkinter import filedialog
import os

CLIENT_FOLDER = r"D:\itay\אקדמיית המתכנתים\CyberCourse\Client files"
SERVER_FOLDER = r"D:\itay\אקדמיית המתכנתים\CyberCourse\Server files"


# ------------------- Server Functions -------------------

def server_thread():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 8081))
    server_socket.listen(5)
    print("Listening for new connections")
    
    client_socket, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")

    while True:
        command = client_socket.recv(1024).decode()
        if not command:
            break

        if command.startswith("UPLOAD"):
            _, file_name = command.split()
            file_path = os.path.join(SERVER_FOLDER, file_name)
            with open(file_path, "wb") as f:
                while True:
                    data = client_socket.recv(1024)
                    if data == b"__END__":
                        break
                    f.write(data)
            print("File uploaded:", file_name)

        elif command.startswith("DOWNLOAD"):
            _, file_name = command.split()
            file_path = os.path.join(SERVER_FOLDER, file_name)
            with open(file_path, "rb") as f:
                while True:
                    data = f.read(1024)
                    if not data:
                        break
                    client_socket.send(data)
            client_socket.sendall(b"__END__")
            print("File sent:", file_name)

# ------------------- Client Functions --------------------

def create_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 8081))
    print("Client connected")
    return client_socket

def upload_file(client_socket, file_path):
    file_name = os.path.basename(file_path)
    client_socket.sendall(f"UPLOAD {file_name}".encode())

    with open(file_path, "rb") as file:
        while True:
            data = file.read(1024)
            if not data:
                break
            client_socket.send(data)
    client_socket.sendall(b"__END__")
    print("Finish sending file")

def download_file(client_socket, file_path):
    file_name = os.path.basename(file_path)
    client_socket.sendall(f"DOWNLOAD {file_name}".encode())

    with open(file_path, "wb") as file:
        while True:
            data = client_socket.recv(1024)
            if data == b"__END__":
                break
            file.write(data)
    print("File downloaded:", file_name)

# ------------------- GUI Class -------------------

class FileTransferApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Download or upload a file")

        self.client_socket = create_client()

        self.client_listbox = tk.Listbox(root, width=40)
        self.server_listbox = tk.Listbox(root, width=40)
        self.server_listbox.grid(row=1, column=0, padx=10, pady=10)
        self.client_listbox.grid(row=1, column=2, padx=10, pady=10)

        tk.Label(root, text="Files in server").grid(row=0, column=0)
        tk.Label(root, text="Your files").grid(row=0, column=2)

        self.upload_button = tk.Button(root, text="Upload file", command=self.upload_file)
        self.upload_button.grid(row=2, column=2, pady=5)

        self.download_button = tk.Button(root, text="Download file", command=self.download_file)
        self.download_button.grid(row=2, column=0, pady=5)

        self.list_files()

        root.mainloop()

    def list_files(self):
        self.server_listbox.delete(0, tk.END)
        self.client_listbox.delete(0, tk.END)

        for file in os.listdir(SERVER_FOLDER):
            self.server_listbox.insert(tk.END, file)

        for file in os.listdir(CLIENT_FOLDER):
            self.client_listbox.insert(tk.END, file)

    def download_file(self):
        selected_index_tuple = self.server_listbox.curselection()
        if not selected_index_tuple:
            print("No file selected for download")
            return

        file_name = self.server_listbox.get(selected_index_tuple[0])
        save_path = os.path.join(CLIENT_FOLDER, file_name)
        print("Downloading", file_name)
        download_file(self.client_socket, save_path)
        self.list_files()

    def upload_file(self):
        selected_index_tuple = self.client_listbox.curselection()
        if not selected_index_tuple:
            print("No file selected for upload")
            return

        file_name = self.client_listbox.get(selected_index_tuple[0])
        file_path = os.path.join(CLIENT_FOLDER, file_name)
        print("Uploading", file_name)
        upload_file(self.client_socket, file_path)
        self.list_files()

# ------------------- Main -------------------

def main():
    t = threading.Thread(target=server_thread, daemon=True)
    t.start()

    root = tk.Tk()
    app = FileTransferApp(root)

if __name__ == '__main__':
    main()