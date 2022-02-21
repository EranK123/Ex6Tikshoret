import threading
import socket

HOST = '127.0.0.1'
PORT = 5001

class Server:

    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(5)
        self.clients = [] #{name, socket}
        self.names = [] #{name, socket}
        # self.conn = False
        # self.async_msgs = {}


    def broadcast(self, msg):
        for client in self.clients:
            client.send(msg)

    # def pr_broadcast(self,from_client, to_client, msg):
    #     for c in self.async_msgs:
    #         if c is to_client:
    #             self.async_msgs.put_msg_by_user("MSG|" + from_client + "|" + msg, to_client)


    def pr_broadcast(self,from_client, to_client, msg):
        for c in self.clients:
            if c is to_client:
                c.send(msg)

    def handle(self, client):
        while True:
            try:
                print("26")
                # start = client.recv(1024)
                # temp = start.decode('utf-8').partition('%')
                # print("temp : ", temp)
                # t0 = temp[0]
                # msg = temp[2]
                msg = client.recv(1024)##.decode('utf-8')
                # print(msg.decode('utf-8'))

                # print("t0: ", t0)
                # print("msg: ", msg)
                if msg.decode('utf-8').startswith('GET_USERS'):
                    print("34")
                    self.print_users(client)
                elif msg.decode('utf-8').startswith('DIS'):
                    print("36")
                    self.dis_user(client)
                    print("{} disconnected".format(client_name(client)))
                # elif msg.decode('ascii').startswith('CON'):
                #     conn = True
                #     connect_name = msg.decode('ascii')[8:]
                #     connect_user(connect_name)
                # elif msg.decode('utf-8').startswith('SEND_ALL'):
                #     print("43")
                #     message = msg.decode('utf-8')[12:]
                #     self.broadcast(message)
                # elif msg.decode('utf-8').startswith('SEND_ONE'):
                #     print("47")
                #     self.pr_broadcast(client, t0, message)

                else:
                    # if len(to) == 1:
                        self.broadcast(msg)
                        # print("68")
                    # self.sock.send((to.encode('utf-8') + "%".encode('utf-8') + msg.encode('utf-8')))
                    # self.sock.send(to.encode('utf-8'))
                    # print("hey!!!!!!!!!")
                    # else:
                    #     print("73")
                    #     self.pr_broadcast(client, to, msg)
                        # self.msg_area.delete('1.0', 'end')
                        # self.to_area.delete('1.0', 'end')
                    # self.sock.se
                        break
                # else:
                #     print("49")
                #     self.broadcast(msg)
            except:
                print("57")
                if client in self.clients:
                    print("59")
                    print(client)
                    index = self.clients.index(client)
                    self.clients.remove(client)
                    client.close()
                    name = self.names[index]
                    print(name)
                    self.broadcast('{} left!'.format(name).encode('utf-8'))
                    self.names.remove(name)
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
        name = client_name(client)
        if name in self.names:
            i = self.names.index(name)
            dis_client = self.clients[i]
            self.clients.remove(dis_client)
            # clients.remove(client)
            dis_client.close()
            self.names.remove(name)
            # client.close()
            exit(0)


    def print_users(self, client):
        for name in self.names:
            client.send("{}\n".format(name).encode('utf-8'))


server = Server(HOST,PORT)
print("Server is running")
server.receive()