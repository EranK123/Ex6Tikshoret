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
        self.udp = UDP()

    def send(self, data, addr=ADDR):
        print("atending", addr)
        msg = self.udp.send_to(data, addr)

    def recv(self, name_file):
        data, addr = self.udp.recv_from()
        return data, addr
