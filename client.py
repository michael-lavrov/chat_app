import socket
import threading

EMPTY_STR = ''
MSG_MAX_LEN = 2048
CODING_STANDARD = 'utf-8'
EMPTY_MSG_STR = "Message is empty"

# Enter the IP of the server
HOST = '127.0.0.1'
PORT = 1234


def listen_for_messages_from_server(client):
    """
    A function that runs in another thread, receives messages from the server
    :param client: The client socket object
    :return: None
    """
    while True:
        message = client.recv(MSG_MAX_LEN).decode(CODING_STANDARD)
        if message != EMPTY_STR:
            sep_ind = int(message[:message.find('~')])
            message = message[len(str(sep_ind))+1:]
            username = message[:sep_ind]
            content = message[sep_ind+1:]
            print(f"[{username}] {content}")

        else:
            print(EMPTY_MSG_STR)


def send_msg_to_server(client):
    """
    Sending messages to the server
    :param client: The client socket object
    :return: None
    """
    while True:

        message = input()
        if message != EMPTY_STR:
            client.sendall(message.encode())
        else:
            print(EMPTY_MSG_STR)


def communicate_to_server(client):
    """
    Responsible to initiate and maintain communication with the server
    :param client: The client socket object
    :return:
    """

    # Sending the username to the server
    while True:
        username = input("Choose a username: ")
        if username == EMPTY_STR:
            print("Username cannot be empty")
        else:
            break

    client.sendall(username.encode())
    threading.Thread(target=listen_for_messages_from_server, args=(client,)).start()
    send_msg_to_server(client)


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
        print("Successfully connected to server")
    except:
        print(f"Unable to connect to server {HOST}, at port {PORT}")

    communicate_to_server(client)


if __name__ == '__main__':
    main()
