import threading
import socket

host = '127.0.0.1'
port = 5001

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(4)

clients = []
names = []
conn = False


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
                dis_user(client)
                print("{} disconnected".format(client_name(client)))
            # elif msg.decode('ascii').startswith('CON'):
            #     conn = True
            #     connect_name = msg.decode('ascii')[8:]
            #     connect_user(connect_name)
            elif msg.decode('ascii').startswith('SEND_ALL'):
                message = msg.decode('ascii')[12:]
                broadcast(message)
            elif msg.decode('ascii').startswith('SEND_ONE'):
                pass
            else:
                broadcast(msg)
        except:
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                name = names[index]
                broadcast('{} left!'.format(name).encode('ascii'))
                names.remove(name)
                break


def receive():
    while True:
        # if conn:
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
        # conn = False


def client_name(client):
    if client in clients:
        index = clients.index(client)
        name = names[index]
        return name


def connect_user(name):
    pass


def dis_user(client):
    name = client_name(client)
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
