import threading
import socket


name = input("Name: ")
host = '127.0.0.1'
port = 5001
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))


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
        if msg[len(name) + 2:].startswith('/'):
            if msg[len(name) + 2:].startswith('/get_users'):
                client.send('GET_USERS'.encode('ascii'))
            elif msg[len(name) + 2:].startswith('/disconnect'):
                client.send('DIS'.encode('ascii'))
            elif msg[len(name) + 2:].startswith('/connect'):
                client.send('{} CON'.format(msg[len(name) + 2 + 10:]).encode('ascii'))
            elif msg[len(name) + 2:].startswith('/set_msg_all'):
                client.send('{} SEND_ALL'.format(msg[len(name) + 2 + 14:]).encode('ascii'))
            elif msg[len(name) + 2:].startswith('/set_msg'):
                client.send('{} SEND_ONE'.format(msg[len(name) + 2 + 10:]).encode('ascii'))

        else:
            client.send(msg.encode('ascii'))


thread1 = threading.Thread(target=receive)
thread1.start()

thread2 = threading.Thread(target=write)
thread2.start()
