import threading
from socket import *
from time import *
import sys
import signal


def get_sys_arguments():
    pass


"""
while(1):
    try:
        message = input("input message: ").encode()
        serverName = 'localhost'
        serverPort = 12000
        clientSocket = socket(AF_INET, SOCK_DGRAM)
        clientSocket.sendto(message, ("date.cs.umass.edu", 8888))
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        print(modifiedMessage.decode())
        clientSocket.close()
    except (Exception, ):
        quit = "QUIT"
        quit.encode()
        clientSocket.sendto(quit, ("date.cs.umass.edu", 8888))


"""

message = None
done = False

def tcp_sender(port, name):
    print("sender thread up and running")
    TIMEOUT = 5
    global done
    global message
    while not done:
        try:
            client_socket = socket(AF_INET, SOCK_DGRAM)
            client_socket.settimeout(1)
            if done == "QUIT":
                done = True
            if message is not None:
                client_socket.sendto(message.encode(), (name, port))
                message = None

            modifiedMessage, serverAddress = client_socket.recvfrom(2048)
            if modifiedMessage:
                print(modifiedMessage.decode())
            sleep(.1)

        except (Exception,):
            pass
    client_socket.close()


def tcp_recieve_input():
    global message
    while True:
        if message is None:
            message = input("input message: ")
        sleep(.1)
        if done:
            exit()

def main():
    port = None
    name = None
    DEBUG = True
    if DEBUG:
        port = 8888
        name = "date.cs.umass.edu"
    else:
        pass

    thread_ids = []

    sender_thread = threading.Thread(target=tcp_sender, args=(port, name))
    input_thread = threading.Thread(target=tcp_recieve_input)
    input_thread.start()
    sender_thread.start()
    sender_thread.join()
    input_thread.join()


#  thread_ids.append(sender_thread)
# thread_ids.append(receiver_thread)


if __name__ == "__main__":
    main()
"""

def send_message(def_message, ip, port, message_socket):
    message_socket.sendto(def_message, (ip, port))


class TcpSender:
    def __init__(self, syn, sequence_number, file, fin):
        # intialize flags
        self.sequence_number = sequence_number
        self.ack_number = None
        self.syn = syn
        self.ack = False
        self.fin = fin
        self.rst = False
        self.file = file

"""

# %%
