import threading
import socket
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog
from tkinter import *

HOST = '127.0.0.1'
PORT = 5001


class Client:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        msg = tkinter.Tk()
        msg.withdraw()
        self.name = ""
        # self.name = simpledialog.askstring("Name", "Set a name", parent=msg)
        # self.name = simpledialog.askstring("Name", "Set a name")
        self.gui = False
        self.running = True
        gui_thread = threading.Thread(target=self.gui_loop)
        # recv_thread = threading.Thread(target=self.receive)
        gui_thread.start()
        # recv_thread.start()

    def gui_loop(self):
        self.window = tkinter.Tk()
        self.window.configure(bg="lightgray")

        self.label = tkinter.Label(self.window, text="Chat:", bg="lightgray")
        self.label.config(font=("Ariel", 12))
        self.label.pack(padx=15, pady=5)

        self.text = tkinter.scrolledtext.ScrolledText(self.window)
        self.text.pack(padx=20, pady=5)
        self.text.config(state='disabled')

        # self.msg = tkinter.Label(self.window, text="Message:", bg="lightgray")
        # self.msg.config(font=("Ariel", 12))
        # self.msg.pack(padx=20, pady=5)

        # self.area = tkinter.Text(self.window, height=3)
        # self.area.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(self.window, text="Send", command=self.write)
        self.send_button.config(font=("Ariel", 12))
        self.send_button.pack(padx=20, pady=5)

        self.users_button = tkinter.Button(self.window, text="Get Users", command=self.get_users)
        self.users_button.config(font=("Ariel", 12))
        self.users_button.pack(padx=20, pady=5)

        self.dis_button = tkinter.Button(self.window, text="Disconnect", command=self.disconnect)
        self.dis_button.config(font=("Ariel", 12))
        self.dis_button.pack(padx=20, pady=5)


        self.login_button = tkinter.Button(self.window, text="Connect", command=self.login)
        self.login_button.config(font=("Ariel", 12))
        self.login_button.pack(padx=20, pady=5)

        self.to_label = tkinter.Label(self.window, text="To(blank to all):", bg="lightgray")
        self.to_label.config(font=("Ariel", 12))
        self.to_label.pack(padx=20, pady=5)
        self.to_area = tkinter.Text(self.window, height=3)
        self.to_area.pack(padx=20, pady=5)


        self.Message_label = tkinter.Label(self.window, text="Message:", bg="lightgray")
        self.Message_label.config(font=("Ariel", 12))
        self.Message_label.pack(padx=20, pady=5)
        self.msg_area = tkinter.Text(self.window, height=3)
        self.msg_area.pack(padx=20, pady=5)

        self.gui = True
        self.window.protocol("VM_DELETE_WINDOW", self.stop)
        self.window.mainloop()

    def stop(self):
        self.running = False
        self.window.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                msg = self.sock.recv(1024).decode('utf-8')
                print(msg)
                if msg == 'NICK':
                    self.sock.send(self.name.encode('utf-8'))##'ASCI'
                else:
                    if self.gui:
                        self.text.config(state='normal')
                        self.text.insert('end', msg)
                        self.text.yview('end')
                        self.text.config(state='disabled')
            except ConnectionError:
                break
            except:
                print("ERROR")
                # print("88")
                self.sock.close()
                break

    def login(self):
        msg = tkinter.Tk()
        msg.withdraw()
        self.name = simpledialog.askstring("Name", "Set a name", parent=msg)
        recv_thread = threading.Thread(target=self.receive)
        recv_thread.start()

    def get_users(self):
            self.sock.send('GET_USERS'.encode('utf-8'))

    def disconnect(self):
        self.sock.send('DIS'.encode('utf-8'))
        self.window.destroy()

    def write(self):
        while True:
            msg = '{}: {}'.format(self.name, self.msg_area.get('1.0', 'end'))
            to = '{}'.format(self.to_area.get('1.0', 'end'))
            self.sock.send(to.encode('utf-8') + "|".encode('utf-8') + msg.encode('utf-8'))
            # self.sock.send(to.encode('utf-8'))
            self.msg_area.delete('1.0', 'end')
            self.to_area.delete('1.0', 'end')
            break
            # print("125")
            # print("msg: ",msg)
            # print()
            # print("to: ", to)
            # print("len to: ", len(to))
            # if msg[len(self.name) + 2:].startswith('/'):
            #     print("81")
            #     if msg[len(self.name) + 2:].startswith('/get_users'):
            #         print("83")
            #         self.sock.send('GET_USERS'.encode('utf-8'))
            #         break
            #     elif msg[len(self.name) + 2:].startswith('/disconnect'):
            #         print("86")
            #         self.sock.send('DIS'.encode('utf-8'))
            #         break
            #     elif msg[len(self.name) + 2:].startswith('/connect'):
            #         print("89")
            #         self.sock.send('{} CON'.format(msg[len(self.name) + 2 + 10:]).encode('utf-8'))
            #         break
            #     elif msg[len(self.name) + 2:].startswith('/set_msg_all'):
            #         print("92")
            #         self.sock.send('{} SEND_ALL'.format(msg[len(self.name) + 2 + 14:]).encode('utf-8'))
            #         break
            #     elif msg[len(self.name) + 2:].startswith('/set_msg'):
            #         print("95")
            #         self.sock.send('{} SEND_ONE'.format(msg[len(self.name) + 2 + 10:]).encode('utf-8'))
            #         break
            # else:
                # if len(to) == 1:
                #     print("149")
                #     self.sock.send(msg.encode('utf-8'))
                #     # self.sock.send(to.encode('utf-8'))
                #     # print("hey!!!!!!!!!")
                #     self.msg_area.delete('1.0', 'end')
                #     self.to_area.delete('1.0', 'end')
                #     # self.sock.se
                #     break

                    # self.sock.sendto(msg.encode('utf-8'), name)

client = Client(HOST, PORT)
# thread1 = threading.Thread(target=receive)
# thread1.start()
#
# thread2 = threading.Thread(target=write)
# thread2.start()