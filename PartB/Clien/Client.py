import threading
import socket
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog
from tkinter import *
import os
import shutil
from ClientFile import ClientFile
# HOST = '127.0.0.1'
HOST = socket.gethostbyname(socket.gethostname())
PORT = 5001


class Client:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.file_name_client = ""
        self.name = ""
        self.data_f = ""
        self.gui = False
        self.running = True
        gui_thread = threading.Thread(target=self.gui_loop)
        gui_thread.start()

    def gui_loop(self):
        self.connect()

        self.window = tkinter.Tk()
        self.window.configure(bg="lightgray")
        self.window.title("Client")

        self.label = tkinter.Label(self.window, text=self.name + " Chat:", bg="lightgray")
        self.label.config(font=("Ariel", 12))
        self.label.pack(padx=15, pady=5)

        self.text = tkinter.scrolledtext.ScrolledText(self.window)
        self.text.pack(padx=20, pady=5)
        self.text.config(state='disabled')

        # self.connect_button = tkinter.Button(self.window, text="Connect", command=self.connect, bg='yellow')
        # self.connect_button.config(font=("Ariel", 12))
        # self.connect_button.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(self.window, text="Send", command=self.write)
        self.send_button.config(font=("Ariel", 12))
        self.send_button.pack(padx=20, pady=5)

        self.users_button = tkinter.Button(self.window, text="Get Users", command=self.get_users)
        self.users_button.config(font=("Ariel", 12))
        self.users_button.pack(padx=20, pady=5)

        self.dis_button = tkinter.Button(self.window, text="Disconnect", command=self.disconnect)
        self.dis_button.config(font=("Ariel", 12))
        self.dis_button.pack(padx=20, pady=5)

        self.get_files_names = tkinter.Button(self.window, text="Get Files", command=self.get_files)
        self.get_files_names.config(font=("Ariel", 12))
        self.get_files_names.pack(padx=20, pady=5)

        self.download_files = tkinter.Button(self.window, text="Download File", command=self.get_name_file)
        self.download_files.config(font=("Ariel", 12))
        self.download_files.pack(padx=20, pady=5)


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


    def get_files(self):
        self.sock.send('GET_FILES'.encode('utf-8'))

    def get_name_file(self):
        msg = tkinter.Tk()
        msg.withdraw()
        file_name_server = simpledialog.askstring("Server File Name", "Set a Server File", parent=msg)
        self.file_name_client = simpledialog.askstring("Client File Name", "Set a Client File", parent=msg)
        self.sock.send(file_name_server.encode('utf-8') + "#".encode('utf-8'))# + self.file_name_client.encode('utf-8'))
        # self.create_file(file_name_client)

        # create a file and save the data from the server file

    def create_file(self, file_name_client):
        file = open(file_name_client, 'wb')
        # client_file = ClientFile()
        # # if self.data_f != "":
        # print("102")
        # msg = client_file.recv()
        file.write(msg.encode('utf-8'))
        file.close()
        print("File Has Been Succesfully!")

    # def get_file(self, file_name_client):
    #     client_file = ClientFile(HOST, PORT)
    #     print("105")
    #     client_file.recv_file(file_name_client)
    #     print("107")
        # file = open(file_name_client, 'wb')
        # if self.data_f != "":
        #     file.write(self.data_f.encode('utf-8'))
        # file.close()
        # print("File Has Been Succesfully!")

    def stop(self):
        self.running = False
        self.window.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        client_file = ClientFile()
        while self.running:
            try:
                # if self.data_f != "":
                print("102")
                msg_udp = client_file.recv()
                print("msg_udp: ", msg_udp)
                msg = self.sock.recv(1024).decode('utf-8')
                if msg == 'NICK':
                    self.sock.send(self.name.encode('utf-8'))##'ASCI'

                elif msg_udp.startswith("data:"):
                    # self.data_f = msg[5:]
                    # self.create_file(self.file_name_client)
                    self.create_file(self.file_name_client)
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
                self.sock.close()
                exit(0)

    def connect(self):
        msg = tkinter.Tk()
        msg.withdraw()
        self.name = simpledialog.askstring("Name", "Set a name", parent=msg)
        recv_thread = threading.Thread(target=self.receive)
        recv_thread.start()

    def get_users(self):
            self.sock.send('GET_USERS'.encode('utf-8'))

    def disconnect(self):
        self.sock.send('DIS'.encode('utf-8'))
        # self.window.destroy()
        self.window.quit()

    def write(self):
        while True:
            msg = '{}: {}'.format(self.name, self.msg_area.get('1.0', 'end'))
            to = '{}'.format(self.to_area.get('1.0', 'end'))
            self.sock.send(to.encode('utf-8') + "|".encode('utf-8') + msg.encode('utf-8'))
            self.msg_area.delete('1.0', 'end')
            self.to_area.delete('1.0', 'end')
            break

client = Client(HOST, PORT)
