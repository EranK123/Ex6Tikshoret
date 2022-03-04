import threading
import socket
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog
from tkinter import *
import os
from PartB.UDP import UDP

# HOST = '127.0.0.1'
HOST = socket.gethostbyname(socket.gethostname())
PORT = 5002
# PORT_SERVER = 5000
ADDR = (HOST, PORT)

class ClientFile:

    def __init__(self):
        print("19")
        self.udp = UDP()

    def send(self, data, addr=ADDR):
        print("atending", addr)
        msg = self.udp.send_to(data, addr)
        # print("msg:" , msg)
        # return msg

    def recv(self, name_file):

        with open(name_file, "w+") as f:
            data, addr = self.udp.recv_from()
            f.write(data)
        return data, addr