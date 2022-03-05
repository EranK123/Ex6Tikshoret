import socket
import threading

from PartA.Clien import Client

# HOST = '127.0.0.1'
HOST = socket.gethostbyname(socket.gethostname())
PORT = 5001

cli1 = Client.Client(HOST, PORT)
gui_threadcli1 = threading.Thread(target=cli1.gui_loop)
gui_threadcli1.start()
