import socket
import threading
import time

EMPTY_STR = ''
MSG_MAX_LEN = 2048
CODING_STANDARD = 'utf-8'
EMPTY_MSG_STR = "Message is empty"
SLEEP_INTERVAL = 3
HEARTBEAT_MSG = "HEARTBEAT_MESSAGE"


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
            content, username = decode_message(message)
            print(f"[{username}] {content}")

        else:
            print(EMPTY_MSG_STR)


def decode_message(message):
    """
    Decodes message that is sent from the server, gives back the username and the content of the message
    :param message:  string
    :return: content, username
    """

    sep_ind = int(message[:message.find('~')])
    message = message[len(str(sep_ind)) + 1:]
    username = message[:sep_ind]
    content = message[sep_ind + 1:]
    return content, username


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

def send_heartbeat(client):
    """
    Sends a heartbeat message to the server every SLEEP_INTERVAL seconds to signal that the client is
    still connected
    :param client: The client socket object
    :return: None
    """
    while True:
        client.sendall(HEARTBEAT_MSG.encode())
        time.sleep(SLEEP_INTERVAL)


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
            print("ERROR: username cannot be an empty string")
            continue

        client.sendall(username.encode())
        while True:
            response = client.recv(MSG_MAX_LEN).decode(CODING_STANDARD)
            break

        content, _ = decode_message(response)
        if content.startswith("ERROR"):
            print(content)
        else:
            print(content)
            break

    threading.Thread(target=send_heartbeat, args=(client,)).start()
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
