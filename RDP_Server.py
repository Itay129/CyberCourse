from pynput import keyboard, mouse
from PIL import Image, ImageTk
import tkinter as tk
import socket
import threading
import json
from io import BytesIO
import RDP_Server_gui
import struct
import queue




def create_server_socket(ip,port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip,port))
    server_socket.listen(1)
    return server_socket
    
    

def accept_client(server_socket):
    client_socket, addr = server_socket.accept()
    print(f"connection created with {addr}")
    return client_socket
    

def on_key_press(key,client_socket):    
        try:
            key = key.char
        except AttributeError:
            key= str(key) 
        print(f'key pressed: {key}')
        message = {"event": "key press",
                    "key": key}
        send_message(client_socket, message)


def on_mouse_move(x, y, client_socket):
    print(f'Pointer moved to ({x}, {y})')
    message = {
                "event": "mouse move",
                "x": x,
                "y": y
                }
    send_message(client_socket, message)

def on_mouse_click(x, y, button, pressed, client_socket):
    if pressed:
        print(f"Mouse {button} button was pressed at ({x}, {y})")
        message = {
                    "event": "mouse button click",
                    "button": str(button),
                    "x": x,
                    "y": y
                    }
        send_message(client_socket, message)


def on_mouse_scroll(x, y, dx, dy, client_socket):
    print(f"Mouse scroll at ({x},{y}) for ({dx},{dy})")
    message = {
                "event": "mouse scroll",
                "x": x,
                "y": y,
                "dx": dx,
                "dy": dy
                }
    send_message(client_socket, message)

def recv_all(sock, length):
    data = b''
    while len(data) < length:
        packet = sock.recv(length - len(data))
        if not packet:
            return None
        data += packet
    return data

def send_message(sock, message_dict):
    message_bytes = json.dumps(message_dict).encode('utf-8')
    length_prefix = struct.pack(">I", len(message_bytes))
    sock.sendall(length_prefix + message_bytes)


class ImageDisplay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Live Screen")

        self.label = tk.Label(self.root)
        self.label.pack()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.closed = False

        self.q = queue.Queue()
        self._poll_queue()


    def on_close(self):
        self.closed = True
        self.root.destroy()

    def _poll_queue(self):

        if self.closed:
            return
        try:
            while True:
                image_bytes = self.q.get_nowait()
                pil_image = Image.open(BytesIO(image_bytes))
                tk_img = ImageTk.PhotoImage(pil_image)
                self.label.configure(image=tk_img)
                self.label.image = tk_img
        except queue.Empty:
            pass
        self.root.after(30, self._poll_queue)

    def start(self):
        self.root.mainloop()


def receive_screenshots(client_socket, display):
    while not display.closed:
        raw_len = recv_all(client_socket, 4)
        if not raw_len:
            print("Client disconnected")
            break
        img_len = struct.unpack(">I", raw_len)[0]
        image_bytes = recv_all(client_socket, img_len)
        if not image_bytes:
            print("Client disconnected")
            break

        try:
            display.q.put_nowait(image_bytes)
        except queue.Full:
            pass



def start_keyboard_listener(client_socket):
    with keyboard.Listener(on_press=lambda key: on_key_press(key, client_socket)) as listener:
        listener.join()

def start_mouse_listener(client_socket):
    with mouse.Listener(on_move=lambda x,y: on_mouse_move(x, y, client_socket), on_click=lambda x,y,button,pressed: on_mouse_click(x, y, button, pressed, client_socket), on_scroll= lambda x,y,dx,dy: on_mouse_scroll(x, y, dx, dy, client_socket)) as listener:
        listener.join()




def main():
    
    RDP_Server_gui.start_App()
    server_socket = create_server_socket(RDP_Server_gui.get_server_ip(), RDP_Server_gui.get_server_port())
    client_socket = accept_client(server_socket)

    display = ImageDisplay()

    keyboard_thread = threading.Thread(target=start_keyboard_listener, args=(client_socket,))
    mouse_thread = threading.Thread(target=start_mouse_listener, args=(client_socket,))
    screenshot_thread = threading.Thread(target=receive_screenshots, args=(client_socket, display), daemon=True)

    keyboard_thread.daemon = True
    mouse_thread.daemon = True
    screenshot_thread.daemon = True 

    keyboard_thread.start()
    mouse_thread.start()
    screenshot_thread.start()

    display.start()

if __name__ == "__main__":
    main()