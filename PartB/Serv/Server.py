import threading
import socket
import os
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog
from tkinter import *
from ServerFile import ServerFile


HOST = socket.gethostbyname(socket.gethostname())
PORT = 5001


class Server:

    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(5)
        self.clients = []
        self.names = []
        self.list_msgs = {}
        self.gui = False
        self.running = True

    def broadcast(self, msg):
        for client in self.clients:
            client.send(msg)

    def pr_broadcast(self, from_client, to_client, msg):
        for c in self.clients:
            name = self.client_name(c)
            if name == to_client:
                c.send(msg.encode('utf-8'))
                from_client.send(msg.encode('utf-8'))

    def handle(self, client):
        while True:
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
                                self.text.insert(tkinter.INSERT,
                                                 "msg for {} is{}num of msgs 1".format(self.client_name(c),
                                                                                       m[2]) + "\n")

                    elif len(server_file_name) != 0:
                        print("88")
                        thread = threading.Thread(target=self.download_file, args=(client, server_file_name))  # start a thread that will work on sending the file
                        thread.start()


                    else:
                        self.pr_broadcast(client, to[:-1], msg)
                        m = msg.partition(":")
                        self.text.insert(tkinter.INSERT,
                                         "msg for {} is{}num of msgs 1".format(self.client_name(client), m[2]) + "\n")

            except:
                if client in self.clients:
                    index = self.clients.index(client)
                    self.clients.remove(client)
                    client.close()
                    name = self.names[index]
                    self.broadcast('{} left!'.format(name).encode('utf-8'))
                    self.names.remove(name)


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
            self.broadcast("{} left!".format(str(name)).encode('utf-8'))
            print("{} Disconnected".format(str(name)))
            self.text.insert(tkinter.INSERT, "{} Disconnected".format(str(name)) + "\n")
            self.text.insert(END, "\n")
            client.close()
            self.clients.remove(client)
            self.names.remove(name)

    def print_users(self, client):
        self.text.insert(tkinter.INSERT, "--Online Users--\n")
        client.send("--Online Users--\n".encode('utf-8'))
        for name in self.names:
            print("{}".format(name))
            self.text.insert(tkinter.INSERT, "client name: " + name)
            self.text.insert(END, "\n")
            client.send("{}\n".format(name).encode('utf-8'))
        self.text.insert(tkinter.INSERT, "num of clients: " + str(len(self.names)) + "\n")
        print("num of users: {}".format(len(self.names)))

    def get_files(self, client):
        dir_path = os.getcwd()
        # dir_path = "..\\PartB\\Serv"
        dir_list = os.listdir(dir_path)
        self.text.insert(tkinter.INSERT, "-- Server File List --\n")
        client.send("--Files List--\n".encode('utf-8'))
        for name in dir_list:
            if name.endswith(".txt"):
                client.send("{}\n".format(name).encode('utf-8'))
                self.text.insert(tkinter.INSERT, "{}\n".format(name))
                # self.text.insert(END, "\n")

    def download_file(self, client, server_file_name):
        """
        This function downloads and sends a file to the client using the class ServerFile we created using the udp
        sockets we created with the RDT we implemented.
        :param client: The client who will get the file
        :param server_file_name: The name of the file
        """
        client.send("Okay#".encode())  # send an Okay message to let the client know we are ready to send the file
        server_file = ServerFile()
        data, addr = server_file.recv()  # get a confirmation message
        percent = 0.5  # percent of the data that will be sent
        if data == "connect":
            file = open(server_file_name, 'r')  # open the file we want to send
            file_data = file.read()
            p_length = int(len(file_data) * percent)  # length of the packet we want to send.
            server_file.send(file_data[:p_length], addr)  # send the first bytes
            client.send("User {} downloaded {}% out of file. Last byte is: {}\n".format(self.client_name(client),
                                                                                        (percent * 100),
                                                                                        p_length).encode('utf-8'))
            self.text.insert(tkinter.INSERT,
                             "User {} downloaded {}% out of file. Last byte is: {}\n".format(self.client_name(client),
                                                                                             (percent * 100), p_length))
            client.send("Click Proceed to continue or Cancel to cancel\n".encode('utf-8'))
            data, _ = server_file.recv()  # if pressed proceed we send the rest
            if data == "proceed":
                server_file.send(file_data[p_length:], addr)  # send the rest
                self.text.insert(tkinter.INSERT, "User {} downloaded 100% out of file. Last byte is: {}\n".format(
                    self.client_name(client), len(file_data)))
                client.send(
                    "You have downloaded 100% out of file. Last byte is:{} \n".format(len(file_data)).encode('utf-8'))
            elif data == "cancel":  # if the client wants to cancel the download we cancel
                self.text.insert(tkinter.INSERT, "{}\n".format("The Download Has Been Canceled"))

        print("Data is sent!")

    def gui_loop(self):
        self.window = tkinter.Tk()
        self.window.configure(bg="lightgray")
        self.window.title("Server")

        # self.text = tkinter.scrolledtext.ScrolledText(self.window)
        self.text = tkinter.Text(self.window, height=30, width=80)
        self.text.pack(padx=20, pady=5)
        # self.text.config(state='disabled')

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


server = Server(HOST, PORT)
print("Server is running")
gui_thread = threading.Thread(target=server.gui_loop)
gui_thread.start()
thread_ser = threading.Thread(target=server.receive)
thread_ser.start()
