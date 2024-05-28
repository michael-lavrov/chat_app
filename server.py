import socket
import threading

HOST = '127.0.0.1'
PORT = 1234
LISTENERS_LIMIT = 5


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")
    except:
        print(f"Unable to connect to host: {HOST}, at port: {PORT}")

    server.listen(LISTENERS_LIMIT)

    while True:
        client, address = server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}")


if __name__ == "__main__":
    main()
