import threading
import socket
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

host = '127.0.0.1'
port = 5001


class Client:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        msg = tkinter.Tk()
        msg.withdraw()
        self.name = simpledialog.askstring("Name", "Set a name", parent=msg)
        self.gui = False
        self.running = True
        gui_thread = threading.Thread(target=self.gui_loop)
        recv_thread = threading.Thread(target=self.receive)
        gui_thread.start()
        recv_thread.start()

    def gui_loop(self):
        self.window = tkinter.Tk()
        self.window.configure(bg="lightgray")
        self.label = tkinter.Label(self.window, text="Chat:", bg="lightgray")
        self.label.config(font=("Ariel", 12))
        self.label.pack(padx=20, pady=5)

        self.text = tkinter.scrolledtext.ScrolledText(self.window)
        self.text.pack(padx=20, pady=5)
        self.text.config(state='disabled')

        self.msg = tkinter.Label(self.window, text="Message:", bg="lightgray")
        self.msg.config(font=("Ariel", 12))
        self.msg.pack(padx=20, pady=5)

        self.area = tkinter.Text(self.window, height=3)
        self.area.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(self.window, text="Send", comand=self.write)
        self.send_button.pack(font=("Ariel", 12))
        self.send_button.pack(padx=20, pady=5)

        self.gui = True
        self.window.protocol("DELETE", self.stop)

    def stop(self):
        self.running = False
        self.window.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                msg = self.sock.recv(1024).decode('ascii')
                if msg == 'NICK':
                    self.sock.send(self.name.encode('ascii'))
                else:
                    if self.gui:
                        self.area.config(state='normal')
                        self.text.insert('end', msg)
                        self.text.yview('end')
                        self.text.config(state='disabled')
            except:
                print("ERROR")
                self.sock.close()
                break

    def write(self):
        while True:
            msg = '{}: {}'.format(self.name, self.area.get('1.0', 'end'))
            if msg[len(self.name) + 2:].startswith('/'):
                if msg[len(self.name) + 2:].startswith('/get_users'):
                    self.sock.send('GET_USERS'.encode('ascii'))
                elif msg[len(self.name) + 2:].startswith('/disconnect'):
                    self.sock.send('DIS'.encode('ascii'))
                elif msg[len(self.name) + 2:].startswith('/connect'):
                    self.sock.send('{} CON'.format(msg[len(self.name) + 2 + 10:]).encode('ascii'))
                elif msg[len(self.name) + 2:].startswith('/set_msg_all'):
                    self.sock.send('{} SEND_ALL'.format(msg[len(self.name) + 2 + 14:]).encode('ascii'))
                elif msg[len(self.name) + 2:].startswith('/set_msg'):
                    self.sock.send('{} SEND_ONE'.format(msg[len(self.name) + 2 + 10:]).encode('ascii'))

            else:
                self.sock.send(msg.encode('ascii'))
                self.area.delete('1.0', 'end')


client = Client(host, port)
# thread1 = threading.Thread(target=receive)
# thread1.start()
#
# thread2 = threading.Thread(target=write)
# thread2.start()
