import socket
import threading

EMPTY_STR = ''
MSG_MAX_LEN = 2048
CODING_STANDARD = 'utf-8'

HOST = '127.0.0.1'
PORT = 1234


def listen_for_messages_from_server(client):

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

    while True:

        message = input("Message: ")
        if message != EMPTY_STR:
            client.sendall(message.encode())
        else:
            print("Message is empty")
            exit(0)


def communicate_to_server(client):

    #TODO: Add an option to retry entering the username

    # Sending the username to the server
    username = input("Choose a username: ")
    #TODO: Username cannot containt '~'
    if username != EMPTY_STR:
        client.sendall(username.encode())
    else:
        print("Username cannot be empty")
        exit(0)

    threading.Thread(target=listen_for_messages_from_server, args=(client, )).start()
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

