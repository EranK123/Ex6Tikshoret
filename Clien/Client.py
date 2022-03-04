import threading
import socket
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog
from tkinter import *
from PartB.Clien import ClientFile
import os
import shutil

# HOST = '127.0.0.1'
HOST = socket.gethostbyname(socket.gethostname())
PORT = 5001


class Client:

    def __init__(self, host, port):
        """
        This init function sets the client with all it's parameters
        :param host: host IP address
        :param port: port number
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # open a tcp socket
        self.sock.connect((host, port))  # connect it to the host and port
        self.file_name_client = ""
        self.name = ""
        self.data_f = ""
        self.gui = False
        self.running = True
        gui_thread = threading.Thread(target=self.gui_loop)  # run a thread on the gui
        gui_thread.start()

    def gui_loop(self):
        """
        This function creates the gui. It sets all the button and text boxes.
        """
        self.connect()  # when the gui is created the connect function is called

        self.window = tkinter.Tk()
        self.window.configure(bg="lightgray")
        self.window.title("Client")

        self.label = tkinter.Label(self.window, text=self.name + " Chat:", bg="lightgray")
        self.label.config(font=("Ariel", 12))
        self.label.pack(padx=15, pady=5)

        self.text = tkinter.scrolledtext.ScrolledText(self.window)
        self.text.pack(padx=20, pady=5)
        self.text.config(state='disabled')

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

    # get the files names from the server
    def get_files(self):
        """
        In case the button GET_FILES is pressed we send to the server a notification it is sent so the server will display the files
        :return:
        """
        self.sock.send('GET_FILES'.encode('utf-8'))

    def get_name_file(self):
        """
        gets the name file from the server that the client wants
        """
        msg = tkinter.Tk()
        msg.withdraw()
        file_name_server = simpledialog.askstring("Server File Name", "Set a Server File", parent=msg)
        self.file_name_client = simpledialog.askstring("Client File Name", "Set a Client File", parent=msg)
        self.sock.send(file_name_server.encode('utf-8') + "#".encode('utf-8'))  # sends the name of the file the
        # client wants to download to the server

    def create_file(self, file_name_client):
        """
        This function creates the file. It opens the file with the name the client wants
        :param file_name_client:
        :return:
        """
        file = open(file_name_client, 'wb')
        if self.data_f != "":
            file.write(self.data_f.encode('utf-8'))
        file.close()
        print("File Has Been Successfully Created!")

    def stop(self):
        """
        This function stops the client socket and closes the window gui
        :return:
        """
        self.running = False
        self.window.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        """
        This function receives all the messages sent by the server.
        :return:
        """
        while self.running:  # while the client is not closed
            try:
                msg = self.sock.recv(1024).decode('utf-8')  # recv all messages
                if msg == 'NICK':
                    self.sock.send(self.name.encode('utf-8'))

                elif msg.startswith("data:"):  # if the message starts with data we know we want to open a file
                    self.data_f = msg[5:]
                    self.create_file(self.file_name_client)  # create the file with the desired name
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
        """
        This function connects the user to the chat. It opens a window to enter a name. After it is entered the user
        will connect to the chat :return:
        """
        msg = tkinter.Tk()
        msg.withdraw()
        self.name = simpledialog.askstring("Name", "Set a name", parent=msg)
        recv_thread = threading.Thread(target=self.receive) # create a thread on the receiving messages function
        recv_thread.start()

    def get_users(self):
        """
        This function sends a notification to get the users from the server if the GET_USERS button is pressed
        :return:
        """
        self.sock.send('GET_USERS'.encode('utf-8'))

    def disconnect(self):
        """
        This function sends a notification to disconnect the client from the chat to the server if the Disconnect
        button is pressed :return:
        """
        self.sock.send('DIS'.encode('utf-8'))
        self.window.quit()

    def write(self):
        """
        This function writes a message to other clients
        """
        while True:
            msg = '{}: {}'.format(self.name, self.msg_area.get('1.0', 'end')) # gets the message from the message
            # text box
            to = '{}'.format(self.to_area.get('1.0', 'end')) # gets the info to who send the message from To text box
            self.sock.send(to.encode('utf-8') + "|".encode('utf-8') + msg.encode('utf-8')) # sends it to the server
            self.msg_area.delete('1.0', 'end')
            self.to_area.delete('1.0', 'end')
            break


client = Client(HOST, PORT)
