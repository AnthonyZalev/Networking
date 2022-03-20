import java.io.*;
import java.net.*;

/**
 * @author V. Arun
 *
 * This class is like "telnet" but using UDP and can be used as a
 * command-line manual test of a UDP-based ASCII protocol.
 */

public class UDPTelnet {
	private static final int MAX_MSG_SIZE = 2048;
	private static final String SERVER = "date.cs.umass.edu";
	private static final int PORT = 19876;
	private static DatagramSocket udpsock = null;

	// Receives datagram and write to standard output
	public static class UDPReader extends Thread {
		public void run() {
			while (true) {
				byte[] msg = new byte[MAX_MSG_SIZE];
				DatagramPacket recvDgram = new DatagramPacket(msg, msg.length);
				try {
					udpsock.receive(recvDgram);
					System.out.write(recvDgram.getData(), 0,
							recvDgram.getLength());
				} catch (IOException e) {
					e.printStackTrace();
					continue;
				}
			}
		}
	}

	// Reads from standard input and sends datagram
	public static void main(String[] args) throws SocketException,
			UnknownHostException, IOException {
		udpsock = new DatagramSocket();
		BufferedReader stdin =
				new BufferedReader(new InputStreamReader(System.in));
		(new UDPReader()).start();
		String input = null;
		while ((input = stdin.readLine()) != null) {
			DatagramPacket sendDgram =
					new DatagramPacket((input + "\n").getBytes(), Math.min(
							input.length() + 1, MAX_MSG_SIZE),
							InetAddress.getByName((args.length > 0 ?
									args[0]
									: SERVER)),
							(args.length > 1 ? Integer.valueOf(args[1])
									: PORT));
			udpsock.send(sendDgram);
		}
	}
}
