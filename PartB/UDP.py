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

class UDP():

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def recv_from(self):

        total_pck = 1
        list_data = []
        while len(list_data) < total_pck:

            data, addr = self.sock.recvfrom(1024)
            msg = data.decode('utf-8').split("&")
            pck = (msg[-1], int(msg[1]))
            if int(msg[2]) > total_pck:
                total_pck = int(msg[2])
            if pck not in list_data: #check this
                list_data.append(pck)
            else:
                print("same msg pck: ", pck)
            print("magg: ", msg)
            f = "msg: " + (data.decode('utf-8'))
            self.sock.sendto(f.encode('utf-8'), addr)
        print("done")
        list_data.sort(key=lambda x: x[1])
        result = ""
        for m in list_data:
            result += m[0]
        print("list_dataa:", list_data)
        print("result: ", result)
        return result

    def send_to(self, data, address):
        print("48")
        packet_size = 5
        seq_num = 0
        list_data = []
        len_data = 0
        if (len(data)%packet_size == 0):
            len_data = len(data)//packet_size
        else:
            len_data = (len(data) // packet_size) + 1
        for i in range(0, len(data), packet_size):
            if (i+packet_size) <= len(data):
                msg = "seq_num" + "&" + str(seq_num) + "&" + str(len_data) + "&" + data[i:i+packet_size]
                # list_data.append(data[i:i+packet_size])
                list_data.append(msg)
            else:

                msg = "seq_num" + "&" + str(seq_num) + "&" + str(len_data) + "&" + data[i:]
                list_data.append(msg)
            seq_num+=1
        print("list data: ", list_data)
        list_seq = [0 for _ in list_data]
        self.sock.settimeout(10)
        done = False
        # i=0
        while not done:
            for msg in list_data:
                self.sock.sendto(msg.encode('utf-8'), address)
            try:
                while not all([1==x for x in list_seq]):

                    data, addr = self.sock.recvfrom(1024)
                    index = data.decode().split("&")[1]
                    list_seq[int(index)] = 1

            except socket.timeout:
                    continue

            done = all([1==x for x in list_seq])
        print("84!")
            # try:
            #     data_, addr = self.sock.recvfrom(1024)
            #     print("data: ", data_)
            #     done = True
            # except socket.timeout:
            #     continue

    def close(self):
        self.sock.close()

    def bind(self, address):
        self.sock.bind(address)

