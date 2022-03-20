import socket
import sys

#filename = sys.argv[1]
filename = "test.jpg"
#clientserverIP = sys.argv[2]
clientserverIP = 'pear.cs.umass.edu'
#clientserverPort = int(sys.argv[3])
clientserverPort = 18765

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((clientserverIP, clientserverPort))
request = "GET " + filename + "\n"
clientSocket.send(request.encode())
initial_read_size = 1024
modifiedSentence = clientSocket.recv(initial_read_size)

# [0] 200 OK
# [1] BODY_BYTE_OFFSET_IN_FILE : 0
# [2] BODY_BYTE_LENGTH: 58241
# [3] blank
# [4] stuff?

parts = modifiedSentence.split(b'\n') # this splits as a bytestream instead of default string
status_code = parts[0]
body_byte_offset_in_file = parts[1]
body_byte_length = int(parts[2][18:])

# Seperate header from body
image_stream = bytearray()
for i in range(3, len(parts)):
    image_stream.extend(parts[i])

# read into body until body_byte_length body size is reached.
while len(image_stream) < body_byte_length:
    image_stream.extend(clientSocket.recv(4096))

# read to file
with open(filename, "wb") as binary_file:
    binary_file.write(image_stream)

#close socket
clientSocket.close()

