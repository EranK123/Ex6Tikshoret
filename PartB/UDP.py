import socket

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5001
ADDR = (HOST, PORT)


class UDP:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # create a udp socket

    def recv_from(self):
        """
        This function receives the data sent by the sender. It gets the data in segments. And sends back the message
        as a confirmation. It will receive messages until the size of the list containing the data segments equals to
        the total pakcets sent
        """
        total_pck = 1  # number of packets
        list_data = []  # list of the packets
        addr = ()
        while len(list_data) < total_pck:

            try:
                data, addr = self.sock.recvfrom(1024)  # receive the data
            except socket.timeout:
                continue
            msg = data.decode('utf-8').split("&")  # we split the message to get all the parameters
            pck = (msg[-1], int(msg[1]))  # last place is the data, [1] place is the seq num
            if int(msg[2]) > total_pck:  # update total packets size
                total_pck = int(msg[2])
            if pck not in list_data:  # if we didnt yet get the message we append
                list_data.append(pck)
            else:
                print("same msg pck: ", pck)
            f = "msg: " + (data.decode('utf-8'))  # sort of ack message
            self.sock.sendto(f.encode('utf-8'), addr)  # send the message
        print("done")
        list_data.sort(key=lambda x: x[1])  # sort the data by seq
        result = ""
        for m in list_data:
            result += m[0]  # construct the data
        return result, addr

    def send_to(self, data, address):
        """
        This function sends
        :param data:
        :param address:
        :return:
        """
        packet_size = 5
        seq_num = 0
        list_data = []
        if len(data) % packet_size == 0:  # if the size of data divides with packet size then we set the current len to len(data) // packet_size
            len_data = len(data) // packet_size
        else:
            len_data = (len(data) // packet_size) + 1  # we set + 1
        for i in range(0, len(data), packet_size):  # iterate over length of data in packet size jumps
            if (i + packet_size) <= len(data):  # we send each time packets size of packet_size
                msg = "seq_num" + "&" + str(seq_num) + "&" + str(len_data) + "&" + data[i:i + packet_size]
                list_data.append(msg)
            else:  # we send the rest
                msg = "seq_num" + "&" + str(seq_num) + "&" + str(len_data) + "&" + data[i:]
                list_data.append(msg)
            seq_num += 1  # add +1 to seq for each message sent
        list_seq = [0 for _ in list_data]  # 1 if arrived 0 if not
        self.sock.settimeout(10)
        done = False
        while not done:
            for msg in list_data:
                self.sock.sendto(msg.encode('utf-8'), address)  # send each constructed message
            try:
                while not all([1 == x for x in list_seq]):  # if not all of the list is 1 we keep getting
                    # information. Can be 0 if we lost the packet. In this case we send it again
                    data, addr = self.sock.recvfrom(1024)
                    index = data.decode().split("&")[1]
                    list_seq[int(index)] = 1  # update the array num in the correct index to 1

            except socket.timeout:  # if the message has not been received
                continue

            done = all([1 == x for x in list_seq])

    def close(self):
        self.sock.close()

    def bind(self, address):
        self.sock.bind(address)
