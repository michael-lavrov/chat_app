import socket
import threading

EMPTY_STR = ''
MSG_MAX_LEN = 2048
CODING_STANDARD = 'utf-8'

#TODO: Add text when client leaves the chat, remove him from dictionary

HOST = '0.0.0.0'
PORT = 1234
LISTENERS_LIMIT = 5

active_users = {}


def make_prompt_msg(username, content):
    sep_ind = len(username)
    final_msg = f"{sep_ind}~{username}~{content}"
    return final_msg

def listen_for_messages(username):
    """
    Receives messages from the client and echoes them to all users
    :param username: Username of a client
    :return: None
    """
    while True:

        message = active_users[username].recv(MSG_MAX_LEN).decode(CODING_STANDARD)
        if message != EMPTY_STR:
            final_msg = make_prompt_msg(username, message)
            send_msg_to_all(final_msg)
        else:
            print(f"The message sent from client {username} is empty")


def send_msg_to_all(message):
    """
    Sends a given message to all active users
    :param message: The message to be sent
    :return: None
    """
    for user in active_users:
        send_msg_to_single_client(user, message)


def send_msg_to_single_client(username, message):
    """
    Sends message to a single client
    :param username: The username of the client
    :param message: The message to be sent
    :return: None
    """
    active_users[username].sendall(message.encode())


def client_handler(client):
    """
    Handles the client's requests, runs on a separate thread.
    :param client: The client socket object
    :return: None
    """
    while True:

        # Receiving username from the client
        username = client.recv(MSG_MAX_LEN).decode(CODING_STANDARD)

        if username != EMPTY_STR:

            if username not in active_users:
                # Adding username to active users dict
                active_users[username] = client
                prompt_msg = make_prompt_msg("SERVER", f"{username} has joined the chat")
                send_msg_to_all(prompt_msg)
                listen_for_messages(username)
                break
            else:
                print(f"{username} is already taken")
        else:
            print("Username is an empty string")

    # Creating a thread to listen to user messages
    threading.Thread(target=listen_for_messages, args=(username, )).start()


def main():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")
    except:
        print(f"Unable to connect to host: {HOST}, at port: {PORT}")
        exit(0)

    server.listen(LISTENERS_LIMIT)

    while True:
        client, address = server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}")
        threading.Thread(target=client_handler, args=(client, )).start()


if __name__ == "__main__":
    main()
