"""
    Echo Client
"""
import socket
import sys
import traceback


def client(msg, log_buffer=sys.stderr):
    """
        Client socket created.
        :param: Message is sent to server
        :return: Message received by server
    """
    server_address = ('localhost', 10000)

    # Create a TCP socket using IPv4 address
    sock = socket.socket(socket.AF_NET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    print('connecting to {0} port {1}'.format(*server_address), file=log_buffer)

    # Connect your socket to the server
    sock.connect((server_address))

    # Accumulate the entire message received back from the server
    received_message = b''

    # Try/finally block exists purely to allow us to close the socket
    # when we are finished with it
    try:
        print('sending "{0}"'.format(msg), file=log_buffer)

        # Send your message to the server here.
        sock.sendall(msg.encode('utf-8'))

        while True:

            # Send message back in 16 byte chunks
            chunk = socket.recv(16)
            received_message += chunk.decode('uft8')

        # Break if message less than 16 bytes
        if len(chunk) < 16:
            break

        # Log each chunk that is received
        print('received "{0}"'.format(chunk.decode('utf8')), file=log_buffer)

    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

    finally:
        # Close your client socket.
        print('closing socket', file=log_buffer)
        sock.close()

    # Return entire reply received from the server
    return received_message


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage = '\nusage: python echo_client.py "this is my message"\n'
        print(usage, file=sys.stderr)
        sys.exit(1)

    msg = sys.argv[1]
    print(f"Message echoed: {client(msg)}")
