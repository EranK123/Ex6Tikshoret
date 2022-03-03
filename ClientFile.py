import threading
import socket
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog
from tkinter import *
import os

# HOST = '127.0.0.1'
HOST = socket.gethostbyname(socket.gethostname())
PORT = 5001
# PORT_SERVER = 5000
ADDR = (HOST, PORT)

class ClientFile:

    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.sock.connect((host, port))
        self.sock.bind((host, port))
        thread = threading.Thread(target=self.recv_file)
        thread.start()

    def recv_file(self, file_name_client):

        file = open(file_name_client, 'wb')
        expecting_seq = 0
        print("27")
        while True:

            msg, addr = self.sock.recvfrom(4096)
            msg = msg.decode()

            seq = msg[0]
            content = msg[1:]

            # Send Acknowledgment to Client
            ack_message = 'Ack' + seq
            print("38")
            self.sock.sendto(ack_message.encode(), ADDR)
            print("40")

            # if the received sequence number is the expected sequence number
            # besara7a el 7eta de msh mgama3ha awy fa 7awel tefhamha enta
            if seq == str(expecting_seq):
                # Print the Content and
                # stdout.write(content)
                file.write(content.encode('utf-8'))
                print("48")
                expecting_seq = 1 - expecting_seq
            else:
                negative_seq = str(1 - expecting_seq)
                ack_message = 'Ack' + negative_seq
                print("53")
                self.sock.sendto(ack_message.encode(), ADDR)
                print("55")

        file.close()
        print("File Has Been Succesfully!")

    # def create_file(self, file_name_client):
        # file = open(file_name_client, 'wb')
        # if self.data_f != "":
        #     file.write(self.data_f.encode('utf-8'))
        # file.close()
        # print("File Has Been Succesfully!")