import tkinter as tk
from PIL import Image, ImageTk





def start_App():
    starting_window = tk.Tk()
    starting_window.title("Server Page")
    starting_window.geometry("1000x800")
    starting_window.configure(background="blue")


    image = Image.open(r"D:\Users\User\Downloads\RDP_Server_text.png")
    window_width = 1840
    window_height = 890
    resized_image = image.resize((window_width, window_height), Image.LANCZOS)
    background_image = ImageTk.PhotoImage(resized_image)
    image_label = tk.Label(starting_window, image=background_image)
    image_label.place(x=0, y=0, relwidth=1, relheight=1)
    

    title_label = tk.Label(starting_window,
                            text="Remote PC Controlling - Server",
                            font=("Arial", 30, "underline"), 
                            bg="lightgreen", 
                            fg="green", 
                            padx=1000, 
                            pady=8, 
                            justify=tk.CENTER, 
                            relief=tk.RAISED, 
                            wraplength=1000)
    title_label.pack(pady=0)

    
    become_server_button = tk.Button(starting_window, text="Control another PC remotely",font=("Arial",20),fg="white", command=lambda: open_server_window(starting_window),bg="blue")
    become_server_button.pack(expand=True)


    starting_window.mainloop()
    return starting_window

def open_server_window(starting_window):
    server_window = tk.Toplevel(starting_window)
    server_window.title("Connect to the PC you want to control")
    server_window.geometry("640x480")
    server_window.configure(background="blanchedalmond")
    

    title_label = tk.Label(server_window, text="Connect to the other PC", font=("Arial", 26), fg="lightgreen", bg="blanchedalmond")
    title_label.pack(pady=50)

    warning_label = tk.Label(server_window, text="Please be careful, by connecting to another PC you get \n a full access and control of the PC\n Please do not make a bad use of the app",font=("Arial", 14), bg="blanchedalmond", fg="red")
    warning_label.pack(pady=10)

    center_frame = tk.Frame(server_window, bg="blanchedalmond")
    center_frame.pack()


    ip_label = tk.Label(center_frame, text="Enter Connection IP Adress", font=("Arial", 16))
    ip_label.grid(row=0, column=0, pady=10)
    ip_entery = tk.Entry(center_frame, width=40)
    ip_entery.grid(row=1, column=0, pady=10)

    port_label = tk.Label(center_frame, text="Enter Connection Port", font=("Arial", 16))
    port_label.grid(row=2, column=0, pady=10)
    port_entery = tk.Entry(center_frame, width=40)
    port_entery.grid(row=3, column=0, pady=10)

    def submit_data():
        global server_ip
        global server_port
        server_ip = ip_entery.get()
        server_port = port_entery.get()

        starting_window.destroy()



        
        
    connect_button = tk.Button(center_frame, text="Start server Connection",font=("Arial", 24),bg="green",fg="white", command=submit_data)
    connect_button.grid(row=4, column=0, pady=30)

    server_window.lift()
    server_window.focus_force()




def get_server_ip():
    return str(server_ip)

def get_server_port():
     try: 
        return int(server_port)
     except ValueError:
          print("Error - Port must be an Integer")
          return


def main():
    start_App() 



if __name__ == "__main__":
    main()