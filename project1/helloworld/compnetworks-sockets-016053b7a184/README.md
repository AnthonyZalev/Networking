[TOC]

# README #

## Getting Started ##

Single machine TCP or UDP:

1. Run TCPServer.java first, then TCPClient.java on the same machine. For UDP, run the corresponding files UDPServer.java and UDPClient.java.
2. Verify that that the "capitalizing" server returns capitalized user input as expected.

Multiple machines: If you have access another physical machine or a virtual machine, you can verify that the above code works exactly as above across a network provided you change the name or IP address of the server in the client from `localhost` to that of the server.

## Bytestream ##

The TCP example doesn't quite illustrate TCP's (reliable) bytestream abstraction. Unlike UDP's (unreliable) datagram abstraction that either delivers all of a datagram or none of a datagram, TCP reliably delivers transmitted in order to the receiver but may do so in arbitrary chunks, e.g., if the sender sends "*I saw a puppy*", the receiver TCP upon the first socket read may just read the first four bytes "I saw" as that is all has arrived up until then or if the size of the array into which the receiver is reading those bytes is of capacity 4, but the remaining bytes are following right behind or have already arrived into the receiver socket just waiting to be read. 

To be able to better appreciate TCP's bytestream abstraction:

1. Start TCPServerByteArray.java, and then TCPClient.java as before.
2. Type a long sentence or cut-paste contents of a file into standard input on the client side.
3. Observe how the server side "trickles" in the bytestream as and when the bytes arrive and are read by the receiver.

## Other examples ##

`PersistentTCPServer.java, PersistentTCPClient.java`: The simple server examples above dealt with exactly one client request at a time before attending to the next client. Refer to the structure of the main `while` loop to observe as much. The `PersistentTCP*` files allow the server to deal with multiple client requests from a single client before moving on to the next client.

`ThreadedPersistentTCPServer.java`: This example extends the previous example to allow multiple clients to be serviced concurrently each being able to send an arbitrary number of requests before quitting.