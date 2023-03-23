# By Yael Vaisberger 211526462
# 26/11/22
import socket
import select
import protocol

SERVER_PORT = 5555
SERVER_IP = "0.0.0.0"
print("Setting up server...")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen()
print("Listening for clients...")
MAX_MSG_LENGTH = 2048
client_sockets = []
messages_to_send = []
# a dictionary that saves which socket is which's client
names_sockets = {}


# sets the name to the socket and adds to the dictionary {name_sockets}
def name_setter(data, address):
    if data[5:-1] in names_sockets:
        reply = "The name is already taken please pick a diffident one "
    else:
        reply = "HELLO " + data[5:]
        names_sockets[data[5:]] = address
    return reply


# returns list of all socket names
def get_names():
    name_list = ""
    if len(names_sockets) != 0:
        for s in names_sockets.keys():
            name_list = name_list + s + " "
    return name_list


# creates a msg to send to another client
def pass_msg(client_input, n):
    socket_name = client_input.split(' ')[1]
    if socket_name in names_sockets.keys():
        address_socket = names_sockets.get(socket_name)
        msg_to_send = client_input.split(' ')[2:]
        msg_to_pass = ''.join(n) + " sent " + ' '.join(msg_to_send)
    else:
        address_socket = " "
        msg_to_pass = "Cant send message to that address"
    return msg_to_pass, address_socket


# while server is up and running
while True:
    read_list = [server_socket] + client_sockets
    ready_to_read, ready_to_write, in_error = select.select(read_list, client_sockets, [])
    for current_socket in ready_to_read:
        if current_socket is server_socket:
            connection, client_address = current_socket.accept()
            print("New client joined!", client_address)
            client_sockets.append(connection)
        else:
            valid, data = protocol.recv_msg(current_socket.recv(1024).decode())
            # checks if command valid
            if not valid:
                msg = "Command not valid, try again"
                messages_to_send.append((current_socket, str(msg)))
                messages_to_send.clear()
            if data == "":
                print("Connection closed", )
                client_sockets.remove(current_socket)
                current_socket.close()
            else:
                connect_socket = current_socket
                if data[0:4] == "NAME":
                    msg = name_setter(data, current_socket)
                if data[0:9] == "GET_NAMES":
                    msg = get_names()
                if data[0:3] == "MSG":
                    name = {i for i in names_sockets if names_sockets[i] == current_socket}
                    msg, address = pass_msg(data, name)
                    if address != " ":
                        connect_socket = address
                if data[0:4] == "EXIT":
                    name = {i for i in names_sockets if names_sockets[i] == current_socket}
                    del (names_sockets[''.join(name)])
                    client_sockets.remove(current_socket)
                    current_socket.close()
                else:
                    messages_to_send.append((connect_socket, str(msg)))
# send a msg to client if there is one
    for message in messages_to_send:
        current_socket, data = message
        if current_socket in ready_to_write:
            current_socket.send(data.encode())
        messages_to_send.remove(message)

if __name__ == "__main__":
    main()
