import threading
import socket
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog
from tkinter import *
import os
from PartB.UDP import UDP

HOST = '127.0.0.1'
# HOST = socket.gethostbyname(socket.gethostname())
PORT = 5001
ADDR = (HOST, PORT)
SEGMENT_SIZE = 20

class ServerFile:

    # def __init__(self, host, port):
    #     self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.sock.connect((host, port))
        # self.sock.bind((host, port))
        # thread = threading.Thread(target=self.send_file)
        # thread.start()

    def send(self, data):
        print("26")
        udp = UDP()
        print("27")
        # udp.bind(ADDR)
        print("28")
        udp.send_to(data, ADDR)
        print("32")