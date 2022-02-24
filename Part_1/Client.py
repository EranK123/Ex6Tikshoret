import threading
import socket

name = input("Name: ")
host = '127.0.0.1'
port = 5001
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

#
def receive():
    while True:
        try:
            msg = client.recv(1024).decode('ascii')
            if msg == 'NICK':
                client.send(name.encode('ascii'))
            else:
                print(msg)
        except:
            print("ERROR")
            client.close()
            break


def write():
    while True:
        msg = '{}: {}'.format(name, input(""))
        client.send(msg.encode('ascii'))


thread1 = threading.Thread(target=receive)
thread1.start()

thread2 = threading.Thread(target=write)
thread2.start()
