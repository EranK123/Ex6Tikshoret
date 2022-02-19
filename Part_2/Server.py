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
        client.send(msg)


def handle(client):
    while True:
        try:
            msg = client.recv(1024)
            if msg.decode('ascii').startswith('GET_USERS'):
                print_users(client)
            elif msg.decode('ascii').startswith('DIS'):
                disconnect_name = msg.decode('ascii')[11:]
                dis_user(disconnect_name)
                print("{} disconnected".format(disconnect_name))
            else:
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


def dis_user(name):
    if name in names:
        i = names.index(name)
        dis_client = clients[i]
        clients.remove(dis_client)
        dis_client.close()
        names.remove(name)


def print_users(client):
    for name in names:
        client.send("{}".format(name).encode('ascii'))


print("Server is running")
receive()
