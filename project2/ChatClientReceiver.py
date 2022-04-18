

from socket import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print ("The server is ready to receive")
bytearray = bytearray()
while True:
    message, clientAddress = serverSocket.recvfrom(100000)
    message = str(len(message))
    serverSocket.sendto(message.encode(), clientAddress)


