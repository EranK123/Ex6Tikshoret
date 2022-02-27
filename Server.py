import threading
import socket
from AsyncMessages import AsyncMessages
import os
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog
from tkinter import *
# HOST = '127.0.0.1'
HOST = socket.gethostbyname(socket.gethostname())
PORT = 5001

class Server():

    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(5)
        self.clients = [] #{name, socket}
        self.names = [] #{name, socket}
        # self.conn = False
        # self.async_msgs = {}
        self.list_msgs = {}
        self.gui = False
        self.running = True
        gui_thread = threading.Thread(target=self.gui_loop)
        gui_thread.start()


    def broadcast(self, msg):
        for client in self.clients:
            client.send(msg)

        # self.list_msgs.put_msg_to_all(msg)

    def pr_broadcast(self,from_client, to_client, msg):
        for c in self.clients:
            name = self.client_name(c)
            if name == to_client:
                c.send(msg.encode('utf-8'))
                from_client.send(msg.encode('utf-8'))
        # self.list_msgs.put_msg_by_user(msg, to_client)

    def handle(self, client):
        while True:
            try:
                start = client.recv(1024)
                temp = start.decode('utf-8')#.partition("|")
                c1 = "|"
                c2 = "#"
                server_file_name = ""
                # client_file_name = ""
                to = ""
                msg = ""
                if c1 in temp:
                    temp = temp.partition("|")
                    to = temp[0]
                    msg = temp[2]
                elif c2 in temp:
                    temp = temp.partition("#")
                    server_file_name = temp[0]
                    # client_file_name = temp[2]
                else:
                    temp = temp.partition("|")
                    msg = temp[0]
                    to = temp[2]


                if msg.startswith('GET_USERS'):
                    self.print_users(client)

                elif msg.startswith('GET_FILES'):
                    self.get_files(client)

                elif msg.startswith('DIS'):
                    self.dis_user(client)
                    print("{} disconnected".format(client_name(client)))

                else:
                    if len(to) == 1:
                        self.broadcast(msg.encode('utf-8'))
                        for c in self.clients:
                            if self.client_name(c) != self.client_name(client):
                                m = msg.partition(":")
                                self.text.insert(tkinter.INSERT, "msg for {} is{}num of msgs 1".format(self.client_name(c),m[2]) + "\n")

                    elif len(server_file_name) != 0:
                        self.download_file(client, server_file_name)

                    else:
                        self.pr_broadcast(client, to[:-1], msg)#.encode('utf-8'))
                        m = msg.partition(":")
                        self.text.insert(tkinter.INSERT, "msg for {} is{}num of msgs 1".format(self.client_name(client) ,m[2]) + "\n")

            except:
                if client in self.clients:
                    index = self.clients.index(client)
                    self.clients.remove(client)
                    client.close()
                    name = self.names[index]
                    self.broadcast('{} left!'.format(name).encode('utf-8'))
                    self.names.remove(name)
                    # self.list_msgs.delete_socket(client)
                    # self.list_msgs.delete_user()


    def receive(self):
        while True:
            client, addr = self.server.accept()


            client.send('NICK'.encode('utf-8'))
            name = client.recv(1024).decode('utf-8')
            print("{} Connected with {}".format(name, str(addr)))
            self.text.insert(tkinter.INSERT, "{} Connected with {}".format(name, str(addr)) + "\n")
            self.text.insert(END, "\n")
            self.names.append(name)
            self.clients.append(client)
            self.broadcast("{} joined!\n".format(name).encode('utf-8'))
            client.send('Connected to the chat\n'.encode('utf-8'))

            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()


    def client_name(self, client):
        if client in self.clients:
            index = self.clients.index(client)
            name = self.names[index]
            return name


    def dis_user(self, client):
        name = self.client_name(client)
        if name in self.names:
            print("{} Disconnected".format(str(name)))
            self.text.insert(tkinter.INSERT, "{} Disconnected".format(str(name)) + "\n")
            self.text.insert(END, "\n")
            client.close()
            self.clients.remove(client)
            self.names.remove(name)
            # self.list_msgs.delete_socket(client)
            # self.list_msgs.delete_user(name)

    def print_users(self, client):
        for name in self.names:
            print("{}".format(name))
            self.text.insert(tkinter.INSERT, "client name: " + name)
            self.text.insert(END, "\n")
            client.send("{}\n".format(name).encode('utf-8'))
        self.text.insert(tkinter.INSERT, "num of clients: " + str(len(self.names)) + "\n")
        print("num of users: {}".format(len(self.names)))


    def get_files(self,client):
        dir_path = os.getcwd()
        dir_list = os.listdir(dir_path)
        self.text.insert(tkinter.INSERT, "-- Server File List --\n")
        for name in dir_list:
            if name.endswith(".txt"):
                client.send("{}\n".format(name).encode('utf-8'))
                self.text.insert(tkinter.INSERT, "{}\n".format(name))
                # self.text.insert(END, "\n")

    def download_file(self, client, server_file_name):
        file = open(server_file_name, 'rb')
        file_data = file.read(1024)
        while file_data:
            # print("file data!!: " ,file_data)
            client.send("data:".encode('utf-8') + file_data)
            file_data = file.read(1024)
        print("Data is sent!")

    def start(self):
        pass

    def gui_loop(self):
        self.window = tkinter.Tk()
        self.window.configure(bg="lightgray")
        self.window.title("Server")

        # self.text = tkinter.scrolledtext.ScrolledText(self.window)
        self.text = tkinter.Text(self.window, height=30, width=80)
        self.text.pack(padx=20, pady=5)
        # self.text.config(state='disabled')

        # self.start_button = tkinter.Button(self.window, text="Start", command=self.start)
        # self.start_button.config(font=("Ariel", 12))
        # self.start_button.pack(padx=20, pady=5)

        self.gui = True
        self.window.protocol("VM_DELETE_WINDOW", self.stop)
        self.window.mainloop()


    def stop(self):
        self.running = False
        self.window.destroy()
        self.sock.close()
        exit(0)


server = Server(HOST,PORT)
print("Server is running")
server.receive()