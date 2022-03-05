import socket
import threading
from PartA.Serv import Server
# HOST = '127.0.0.1'
HOST = socket.gethostbyname(socket.gethostname())
PORT = 5001

ser = Server.Server(HOST, PORT)
gui_thread = threading.Thread(target=ser.gui_loop)
gui_thread.start()
thread_ser = threading.Thread(target=ser.receive)
thread_ser.start()