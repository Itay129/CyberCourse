import socket
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController
from PIL import ImageGrab
import threading
import json
import io
import RDP_Client_gui
import struct
import time



def create_client(ip,port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip,port))
    print("client connected")
    return client_socket

def recv_all(sock, length):
    data = b""
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise ConnectionError("Socket closed before receiving all data")
        data += more
    return data

def receive_message(client_socket):
    raw_len = recv_all(client_socket, 4)
    msg_len = struct.unpack(">I", raw_len)[0]
    message_bytes = recv_all(client_socket, msg_len)
    message_str = message_bytes.decode('utf-8')
    message_dict = json.loads(message_str)
    return message_dict

def receive_and_redirect_data(client_socket, keyboard, mouse):
    while True:
        try:
            try:
                data = receive_message(client_socket)
            except ConnectionError:
                print("Connection lost")
                client_socket.close()
                break
            except json.JSONDecodeError:
                print("Invalid JSON received")
                continue
                

            event = data.get("event")

            if event == "mouse move":
                x = int(data["x"])
                y = int(data["y"])
                mouse_move(mouse, x, y)

            elif event == "mouse button click":
                button = data["button"]
                x = data["x"]
                y = data["y"]
                click_mouse_button(mouse, button, x, y)

            elif event == "mouse scroll":
                x = data["x"]
                y = data["y"]
                dx = data["dx"]
                dy = data["dy"]
                mouse_scroll(mouse, x, y, dx, dy)
                
            elif event == "key press":
                key = data["key"]
                key_press(keyboard, key)

            else:
                print(f"Unknown event: {event}")

        except (ConnectionError, OSError):
            print("Connection lost while sending screenshots")
            break




def key_press(keyboard, key):
    key = str(key)
    if key.startswith("Key."):
        key_name = key.split(".", 1)[1]
        special = getattr(Key, key_name, None)
        if special:
            keyboard.press(special)
            keyboard.release(special)
            return
    if len(key) == 1:
        keyboard.press(key)
        keyboard.release(key)
    else:
        ks2 = key.replace("key pressed: ", "")
        if len(ks2) == 1:
            keyboard.press(ks2)
            keyboard.release(ks2)
    
    key = str(key).replace("key pressed: ","")
    keyboard.press(str(key))
    keyboard.release(str(key))

def click_mouse_button(mouse, button, x, y):
    print(f"mouse button clicked on other pc {button} at({x,y})")
    mouse_move(mouse, x, y)
    if "left" in str(button):
        btn = Button.left
    elif "right" in str(button):
        btn = Button.right
    else:
        btn = Button.middle

    mouse.click(btn, 1)

def mouse_scroll(mouse, x, y, dx, dy):
    mouse_move(mouse, x, y)
    mouse.scroll(dx, dy)

def mouse_move(mouse, x, y):
    mouse.position = (x,y)

def start_keyboard_operations():
    keyboard = KeyboardController()
    return keyboard

def start_mouse_operations():
    mouse = MouseController()
    return mouse

def send_screenshots(client_socket):
    while True:
        try:
            screenshot = ImageGrab.grab()
            byte_arr = io.BytesIO()
            screenshot = screenshot.resize((1280, 720))
            screenshot.save(byte_arr, format='JPEG', quality=60)
            image_bytes = byte_arr.getvalue()

            client_socket.sendall(struct.pack(">I",len(image_bytes)))
            client_socket.sendall(image_bytes)

            time.sleep(0.045)

        except (ConnectionError, OSError):
            print("Connection lost while sending screenshots")
            break



def main():

    RDP_Client_gui.start_App()
    client_socket = create_client(RDP_Client_gui.get_client_ip(), RDP_Client_gui.get_client_port())

    keyboard = start_keyboard_operations()
    mouse = start_mouse_operations()
    actions = threading.Thread(target = receive_and_redirect_data, args=(client_socket, keyboard, mouse))
    rapid_send_screenshots = threading.Thread(target = send_screenshots, args=(client_socket,))
    
    actions.start()
    rapid_send_screenshots.start()

    rapid_send_screenshots.join()
    

if __name__ == "__main__":
    main()