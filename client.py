import socket
import threading

EMPTY_STR = ''
MSG_MAX_LEN = 2048
CODING_STANDARD = 'utf-8'

# Enter the IP of the server
HOST = '192.168.68.105'
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
            split_msg = message.split('~')
            username = split_msg[0]
            content = EMPTY_STR
            for i in range(1, len(split_msg)):
                content += split_msg[i]

            print(f"[{username}] {content}")

        else:
            print("Message is empty")


def send_msg_to_server(client):
    """
    Sending messages to the server
    :param client: The client socket object
    :return: None
    """
    while True:

        message = input("Message: ")
        if message != EMPTY_STR:
            client.sendall(message.encode())
        else:
            print("Message is empty")
            exit(0)


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
        elif '~' in username:
            print("Username cannot contain '~'")
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
