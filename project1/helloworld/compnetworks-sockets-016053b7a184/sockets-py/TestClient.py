import socket
print('starting')
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverName = 'date.cs.umass.edu'
address = (serverName, 18765)
clientSocket.connect(address)
sentence = ('GET redsox.jpg\n'.encode())

clientSocket.send(sentence)
something = clientSocket.recv(1024)
print(something.decode())