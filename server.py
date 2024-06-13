import socket
import threading
import time
from dataclasses import dataclass

EMPTY_STR = ''
MSG_MAX_LEN = 2048
CODING_STANDARD = 'utf-8'
HEARTBEAT_MSG = "HEARTBEAT_MESSAGE"
HEARTBEAT_INTERVAL = 5


HOST = '0.0.0.0'
PORT = 1234
LISTENERS_LIMIT = 5

active_users = {}
heartbeats = {}


@dataclass
class Client:
    username: str
    client_socket: socket
    last_hb_time: time
    thread: threading


def monitor_heartbeats():
    """
    Runs in a separate thread, checks whether the clients are still active.
    :return: None
    """

    while True:
        current_time = time.time()
        users_to_terminate = []
        for user in active_users:
            if current_time - active_users[user].last_hb_time > HEARTBEAT_INTERVAL:
                # Heartbeat was not sent
                users_to_terminate.append(user)
                active_users[user].client_socket.close()
                active_users[user].thread.join()

        for user in users_to_terminate:
            del active_users[user]
            time_out_msg = f"{user} has left the chat"
            print(time_out_msg)
            send_msg_to_all(make_prompt_msg("SERVER", time_out_msg))

        time.sleep(HEARTBEAT_INTERVAL)


def make_prompt_msg(username, content):
    """
    Makes the message in prompt format before sending it to clients.
    """
    sep_ind = len(username)
    final_msg = f"{sep_ind}~{username}~{content}"
    return final_msg


def listen_for_messages(username):
    """
    Receives messages from the client and echoes them to all users
    :param username: Username of a client
    :return: None
    """
    active_users[username].last_hb_time = time.time()
    while True:

        try:
            message = active_users[username].client_socket.recv(MSG_MAX_LEN).decode(CODING_STANDARD)

            if message != EMPTY_STR:
                if message == HEARTBEAT_MSG:
                    active_users[username].last_hb_time = time.time()
                else:
                    final_msg = make_prompt_msg(username, message)
                    send_msg_to_all(final_msg)
            else:
                print(f"The message sent from client {username} is empty")

        except Exception as e:
            print(f"Exception in listening to user {username}: {e}")
            break

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
    active_users[username].client_socket.sendall(message.encode())


def client_handler(client_socket):
    """
    Handles the client's requests, runs on a separate thread.
    :param client_socket: The client socket object
    :return: None
    """
    while True:

        # Receiving username from the client
        username = client_socket.recv(MSG_MAX_LEN).decode(CODING_STANDARD)

        if username not in active_users:
            # Adding username to active users dict
            prompt_msg = make_prompt_msg("SERVER", f"{username} has joined the chat")
            send_msg_to_all(prompt_msg)
            break
        else:
            error_msg = make_prompt_msg("SERVER", f"ERROR: {username} is already taken")
            client_socket.sendall(error_msg.encode())

    success_msg = make_prompt_msg("SERVER", "Connection was successful")
    client_socket.sendall(success_msg.encode())
    # Creating a thread to listen to user messages
    thread = threading.Thread(target=listen_for_messages, args=(username, ))
    client = Client(username=username, client_socket=client_socket, last_hb_time=time.time(), thread=thread)
    active_users[username] = client
    thread.start()


def main():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")
    except Exception as e:
        print(f"Unable to bind {(HOST, PORT)}: {e}")
        exit(0)

    server.listen(LISTENERS_LIMIT)

    threading.Thread(target=monitor_heartbeats).start()
    while True:
        client, address = server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}")
        threading.Thread(target=client_handler, args=(client, )).start()


if __name__ == "__main__":
    main()
