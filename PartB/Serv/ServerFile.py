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
ADDR = (HOST, PORT)
SEGMENT_SIZE = 20


class ServerFile:

    def __init__(self):
        print("26")
        self.udp = UDP()
        self.udp.bind(ADDR)
        print("bound to ", ADDR)

    def recv(self):
        # data = ""
        # addr = ()
        data, addr = self.udp.recv_from()
        print("32")
        return data, addr

    def send(self, data, addr):
        self.udp.send_to(data, addr)
