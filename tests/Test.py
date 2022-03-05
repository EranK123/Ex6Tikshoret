import threading
import time
import unittest
import socket
from PartA.Serv import Server
from PartA.Clien import Client

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5001


class Test(unittest.TestCase):

    def test_mun_clients_server(self):
        ser = Server.Server(HOST, PORT)
        gui_thread = threading.Thread(target=ser.gui_loop)
        gui_thread.start()
        time.sleep(1)
        cli1 = Client.Client(HOST, PORT)
        gui_threadcli1 = threading.Thread(target=cli1.gui_loop)

        time.sleep(1)
        cli2 = Client.Client(HOST, PORT)
        gui_threadcli2 = threading.Thread(target=cli2.gui_loop)

        thread_ser = threading.Thread(target=ser.receive)
        thread_ser.start()
        gui_threadcli1.start()
        gui_threadcli2.start()
        time.sleep(10)
        self.assertEqual(len(ser.clients), 2)

    def test_get_users(self):
        ser = Server.Server(HOST, PORT)
        gui_thread = threading.Thread(target=ser.gui_loop)
        gui_thread.start()

        time.sleep(1)
        cli1 = Client.Client(HOST, PORT)
        gui_threadcli1 = threading.Thread(target=cli1.gui_loop)

        time.sleep(1)
        cli2 = Client.Client(HOST, PORT)
        gui_threadcli2 = threading.Thread(target=cli2.gui_loop)

        thread_ser = threading.Thread(target=ser.receive)
        thread_ser.start()
        gui_threadcli1.start()
        gui_threadcli2.start()

        time.sleep(10)
        self.assertEqual(ser.names[0], cli1.name)
        self.assertEqual(ser.names[1], cli2.name)

    def test_file_data(self):
        ser = Server.Server(HOST, PORT)
        gui_thread = threading.Thread(target=ser.gui_loop)
        gui_thread.start()

        time.sleep(1)
        cli1 = Client.Client(HOST, PORT)
        gui_threadcli1 = threading.Thread(target=cli1.gui_loop)

        time.sleep(1)
        thread_ser = threading.Thread(target=ser.receive)
        thread_ser.start()
        gui_threadcli1.start()
        time.sleep(8)
        data_serv = ser.data_file('f.txt').decode('utf-8')
        time.sleep(10)
        self.assertEqual(data_serv, cli1.data_f)

    def test_msg(self):
        ser = Server.Server(HOST, PORT)
        gui_thread = threading.Thread(target=ser.gui_loop)
        gui_thread.start()

        time.sleep(1)
        cli1 = Client.Client(HOST, PORT)
        gui_threadcli1 = threading.Thread(target=cli1.gui_loop)

        time.sleep(1)
        thread_ser = threading.Thread(target=ser.receive)
        thread_ser.start()
        gui_threadcli1.start()

        time.sleep(12)

        self.assertEqual('hey' in cli1.msg, True)
