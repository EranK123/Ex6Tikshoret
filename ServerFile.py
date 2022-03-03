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
ADDR = (HOST, PORT)
SEGMENT_SIZE = 20

class ServerFile:

    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.sock.connect((host, port))
        self.sock.bind((host, port))
        thread = threading.Thread(target=self.send_file)
        thread.start()


    def send_file(self, server_file_name):
        print("23")
        offset = 0
        seq = 0
        # with open(server_file_name) as f:
        #     print("27")
        file = open(server_file_name, 'rb')
        content = file.read(1024).decode('utf-8')
        print("content: ", content)

        while offset < len(content):
            print("32")
            if offset + SEGMENT_SIZE > len(content):
                print("34")
                segment = content[offset:]
            else:
                print("35")
                segment = content[offset:offset + SEGMENT_SIZE]
            offset += SEGMENT_SIZE

            ack_received = False
            while not ack_received:
                print("41")
                message = str(seq) + segment
                print("msg: ", message)
                self.sock.sendto(message.encode('utf-8'), ADDR)
                print("48")
                try:
                    print("50")
                    message, address = self.sock.recvfrom(4096)
                    received_message = message.decode('utf-8')
                except timeout:
                    print("Timeout")
                else:
                    print("56")
                    print("message: ", message)
                    ack_seq = message[3]
                    print("ack_seq: ", ack_seq)
                    print("seq: ", seq)
                    print("str(seq): ", str(seq))
                    if ack_seq == str(seq):  # assuming max number of ACKs is 10
                        ack_received = True
                    # break
            seq = 1 - seq

