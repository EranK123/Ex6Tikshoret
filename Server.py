import threading
import socket
from AsyncMessages import AsyncMessages
HOST = '127.0.0.1'
PORT = 5001

class Server(Asyn):

    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(5)
        self.clients = [] #{name, socket}
        self.names = [] #{name, socket}
        # self.conn = False
        # self.async_msgs = {}
        self.list_msgs = AsyncMessages()


    def broadcast(self, msg):
        for client in self.clients:
            client.send(msg)
        self.list_msgs.put_msg_to_all(msg)

    def pr_broadcast(self,from_client, to_client, msg):
        for c in self.clients:
            name = self.client_name(c)

            if name == to_client:
                c.send(msg.encode('utf-8'))
                from_client.send(msg.encode('utf-8'))
        self.list_msgs.put_msg_by_user(msg, to_client)

    def handle(self, client):
        while True:
            try:
                start = client.recv(1024)
                temp = start.decode('utf-8').partition("|")

                if len(temp[1]) != 0:
                    to = temp[0]
                    msg = temp[2]
                else:
                    msg = temp[0]
                    to = temp[2]

                if msg.startswith('GET_USERS'):
                    self.print_users(client)

                elif msg.startswith('DIS'):
                    self.dis_user(client)
                    print("{} disconnected".format(client_name(client)))

                else:
                    if len(to) == 1:
                        self.broadcast(msg.encode('utf-8'))

                    else:
                        self.pr_broadcast(client, to[:-1], msg)#.encode('utf-8'))

            except:
                if client in self.clients:
                    index = self.clients.index(client)
                    self.clients.remove(client)
                    client.close()
                    name = self.names[index]
                    self.broadcast('{} left!'.format(name).encode('utf-8'))
                    self.names.remove(name)
                    self.list_msgs.delete_socket(client)
                    self.list_msgs.delete_user()
                    break

    # def handle(client):
    #     while True:
    #         try:
    #             msg = client.recv(1024)
    #             print(f"{names[clients.index(client)]} says {msg}")
    #             # print("{} says {}".format(names[clients.index(client)], msg))
    #             broadcast(msg)
    #         except:
    #             index = clients.index(client)
    #             clients.remove(client)
    #             client.close()
    #             name = names[index]
    #             names.remove(name)
    #             break


    def receive(self):
        while True:
            # if conn:
            client, addr = self.server.accept()
            print("Connected with {}".format(str(addr)))

            client.send('NICK'.encode('utf-8'))
            name = client.recv(1024).decode('utf-8')
            self.names.append(name)
            self.clients.append(client)
            self.list_msgs.add_new_socket(client)
            self.list_msgs.add_new_socket_by_user(name)
            print("Nickname is {}".format(name))
            self.broadcast("{} joined!\n".format(name).encode('utf-8'))
            client.send('Connected to the chat\n'.encode('utf-8'))

            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()
            # conn = False


    def client_name(self, client):
        if client in self.clients:
            index = self.clients.index(client)
            name = self.names[index]
            return name


    def connect_user(name):
        pass


    def dis_user(self, client):
        name = self.client_name(client)
        if name in self.names:
            client.close()
            clients.remove(client)
            self.names.remove(name)
            self.list_msgs.delete_socket(client)
            self.list_msgs.delete_user(name)

    def print_users(self, client):
        for name in self.names:
            client.send("{}\n".format(name).encode('utf-8'))


server = Server(HOST,PORT)
print("Server is running")
server.receive()