import socket
from socket import *
import sys
import threading
import time

def make_udp_request(file_name, server_name, server_port):
    """
    :param file_name: file requesting
    :param server_name: name of server
    :param server_port: port number
    :return: 4096 length byte stream and server address or return -1 on fail
    """
    try:
        client_socket = socket(AF_INET, SOCK_DGRAM)
        request = "GET " + file_name + ".torrent\n"
        client_socket.sendto(request.encode(), (server_name, server_port))
        client_socket.settimeout(30)
        message, server_address = client_socket.recvfrom(4096)

        return message, server_address
    except (Exception,):
        return -1


def request_tracker_for_peers(file_name, server_name, server_port):
    """
    :param file_name:
    :param server_name:
    :param server_port:
    :return: dictionary of num block, file size, and 2 peers IP and port's or -1 on fail.
    """

    # Keep on making UDP calls tills I get my block
    request = -1
    while request == -1:
        request = make_udp_request(file_name, server_name, server_port)

    message = request[0]
    # server_address = request[1]

    # [0] NUM_BLOCKS: number of blocks in requested file
    # [1] FILE_SIZE: size of entire file in bytes
    # [2] IP1: 128.119.245.20 identify IP address of first peer
    # [3] PORT1: 3456 identify port number of second peer
    # [4] IP2: 128.119.245.20 identify IP address of second peer
    # [5] PORT2: 4321 identify Port number of second peer

    parts = message.decode().split('\n')  # split on end-line characters
    num_blocks = parts[0].split(':')[1][1:]
    file_size = parts[1].split(':')[1][1:]
    ip1 = parts[2].split(':')[1][1:]
    port1 = parts[3].split(':')[1][1:]
    ip2 = parts[4].split(':')[1][1:]
    port2 = parts[5].split(':')[1][1:]

    return {'num_blocks': int(num_blocks),
            'file_size': int(file_size),
            'IP1': ip1,
            'port1': int(port1),
            'IP2': ip2,
            'port2': int(port2)}


def make_peer_tcp_block_request(file_name, ip_address, port, block_number):
    """
     :param file_name:
     :param ip_address:
     :param port:
     :param block_number:
     :return: byte stream of that block, and offset. or if fail return -1 as an error code.
     """
    try:
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.settimeout(20)
        client_socket.connect((ip_address, port))
        request = "GET " + file_name + ":" + str(block_number) + "\n"
        client_socket.send(request.encode())
        initial_message = bytearray()
        while len(initial_message) < 1024:
            char = client_socket.recv(1024)
            initial_message.extend(char)

        # [0] 200 OK
        # [1] BODY_BYTE_OFFSET_IN_FILE : 0
        # [2] BODY_BYTE_LENGTH: 58241
        # [3] blank
        # [4] stuff?

        parts = initial_message.split(b'\n\n', 1)  # this splits as a bytestream instead of default string
        header = parts[0]
        header = header.split(b'\n')
        # status_code = header[0]
        body_byte_offset_in_file = int(header[1].split(b": ")[1])
        body_byte_length = int(header[2].split(b": ")[1])

        block_stream = parts[1]
        while len(block_stream) < body_byte_length:
            block_stream.extend(client_socket.recv(body_byte_length - len(block_stream)))

        return block_stream, body_byte_offset_in_file
    except ValueError:
        print("bad header format")
        return -1
    except (Exception,):
        print("something else")
        return -1


def main():
    filename = sys.argv[1]
    # filename = "redsox.jpg"
    server_name = sys.argv[2]
    # server_name = 'date.cs.umass.edu'
    server_port = int(sys.argv[3])
    # server_port = 19876

    peers = request_tracker_for_peers(filename, server_name, server_port)
    image_stream = bytearray()

    for i in range(peers['num_blocks']):
        print(i)
        request = -1
        while request == -1:
            request = make_peer_tcp_block_request(filename, peers['IP1'], peers['port1'], i)

        block_bytestream = request[0]
        # block_offset = request[1]
        image_stream.extend(block_bytestream)
        print(len(image_stream))

    with open(filename, "wb") as binary_file:
        binary_file.write(image_stream)


if __name__ == "__main__":
    main()

# %%
