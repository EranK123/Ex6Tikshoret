import threading
import socket

host = '127.0.0.1'
port = 5001

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(4)

clients = []
names = []


def broadcast(msg):
    for client in clients:
        client.sed(msg)


def handle(client):
    while True:
        try:
            msg = client.recv(1024)
            broadcast(msg)
        except:
            index = client.index(client)
            clients.remove(client)
            client.close()
            name = names[index]
            broadcast('{} left!'.format(name).encode('ascii'))
            names.remove(name)
            break


def receive():
    while True:
        client, addr = server.accept()
        print("Connected with {}".format(str(addr)))

        client.send('NICK'.encode('ascii'))
        name = client.recv(1024).decode('ascii')
        names.append(name)
        clients.append(client)
        print("Nickname is {}".format(name))
        broadcast("{} joined!".format(name).encode('ascii'))
        client.send('Connected to the chat'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server is running")
receive()
