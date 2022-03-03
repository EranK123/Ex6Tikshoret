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
# PORT_SERVER = 5000
ADDR = (HOST, PORT)

class ClientFile:

    def recv(self):
        print("19")
        udp = UDP()
        udp.bind(ADDR)
        msg = udp.recv_from()
        print("msg:" , msg)
        return msg