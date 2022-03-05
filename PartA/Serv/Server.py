import threading
import socket
import os
import os.path
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog
from tkinter import *
from PartB.Serv import ServerFile
# HOST = '127.0.0.1'
HOST = socket.gethostbyname(socket.gethostname())
PORT = 5001

class Server():

    def __init__(self, host, port):
        """
          This init function sets the server with all it's parameters
          :param host: host IP address
          :param port: port number
          """
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(5)
        self.clients = []
        self.names = []
        self.list_msgs = {}
        self.gui = False
        self.running = True


    def broadcast(self, msg):
        """
           Sends a message to all the clients in the chat
           :param msg: The msg a client wishes to send to all others
           """
        for client in self.clients:
            client.send(msg)


    def pr_broadcast(self,from_client, to_client, msg):
        """
           Sends a private message to one of the client
           :param from_client: The client who sends the message
           :param to_client: The client who gets the message
           :param msg: the msg a client wishes to send
           """
        for c in self.clients:
            name = self.client_name(c)
            if name == to_client:
                c.send(msg.encode('utf-8'))
                from_client.send(msg.encode('utf-8'))

    def handle(self, client):
        """
          This function handles the messages sent by the clients
          """
        while self.running:
            try:
                start = client.recv(1024)
                temp = start.decode('utf-8')
                c1 = "|"
                c2 = "#"
                server_file_name = ""
                to = ""
                msg = ""
                if c1 in temp:
                    temp = temp.partition("|")
                    to = temp[0]
                    msg = temp[2]
                elif c2 in temp:
                    temp = temp.partition("#")
                    server_file_name = temp[0]
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
                    # self.broadcast('{} left!'.format(name).encode('utf-8'))
                    self.names.remove(name)


    def receive(self):
        """
          This function accepts new connections which are new clients wanting to connect to the chat
          :return:
          """
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
        """
        This function find the name of a client
        """
        if client in self.clients:
            index = self.clients.index(client)
            name = self.names[index]
            return name


    def dis_user(self, client):
        """
           This function disconnects a user from the chat
           :param client: client that will be disconnected
           """
        name = self.client_name(client)
        if name in self.names:
            self.broadcast("{} left!".format(str(name)).encode('utf-8'))
            print("{} Disconnected".format(str(name)))
            self.text.insert(tkinter.INSERT, "{} Disconnected".format(str(name)) + "\n")
            self.text.insert(END, "\n")
            client.close()
            self.clients.remove(client)
            self.names.remove(name)

    def print_users(self, client):
        """
           This function prints all users in client gui and server gui
           """

        self.text.insert(tkinter.INSERT, "--Online Users--\n")
        # name = self.client_name(client)
        client.send("--Online Users--\n".encode('utf-8'))
        for name in self.names:
            print("{}".format(name))
            self.text.insert(tkinter.INSERT, "client name: " + name)
            self.text.insert(END, "\n")
            client.send("{}\n".format(name).encode('utf-8'))
        self.text.insert(tkinter.INSERT, "num of clients: " + str(len(self.names)) + "\n")
        print("\nnum of users: {}".format(len(self.names)))


    def get_files(self,client):
        """
           This function displays the file list in the client and the server:
           """
        dir_path = os.getcwd()
        dir_list = os.listdir(dir_path)
        self.text.insert(tkinter.INSERT, "-- Server File List --\n")
        client.send("--Files List--\n".encode('utf-8'))
        for name in dir_list:
            if name.endswith(".txt"):
                client.send("{}\n".format(name).encode('utf-8'))
                self.text.insert(tkinter.INSERT, "{}\n".format(name))

    def download_file(self, client, server_file_name):
        """
           This function downloads the file from the server and sends it's content to the client
           :param client:
           :param server_file_name:
           :return:
           """
        file = open(server_file_name, 'rb')
        file_data = file.read(1024)
        while file_data:
            client.send("data:".encode('utf-8') + file_data)
            file_data = file.read(1024)
        print("Data is sent!")

    def data_file(self, server_file_name):

        file = open(server_file_name, 'rb')
        file_data = file.read(1024)
        print("file data$: ", file_data)
        return file_data

    def gui_loop(self):
        """
           This function handles the gui of the server
           """
        self.window = tkinter.Tk()
        self.window.configure(bg="lightgray")
        self.window.title("Server")
        self.text = tkinter.Text(self.window, height=30, width=80)
        self.text.pack(padx=20, pady=5)

        self.stop_button = tkinter.Button(self.window, text="Stop", command=self.stop)
        self.stop_button.config(font=("Ariel", 12))
        self.stop_button.pack(padx=20, pady=5)

        self.gui = True
        self.window.mainloop()


    def stop(self):
        self.running = False
        self.server.close()
        self.window.destroy()
        # exit(0)