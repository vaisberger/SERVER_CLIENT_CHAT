# By Yael Vaisberger 211526462
# 26/11/22
import msvcrt
import socket
import protocol
import select


my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.connect(("127.0.0.1", 5555))
messages_to_send = []
EXIT = False
print("pls enter message", flush=True)
# while the socket is running
while not EXIT:
    user_input = ''
    ch = ''
    msg_done = False
    # a loop to get client's request
    while True:
        if msvcrt.kbhit():
            ch = msvcrt.getch().decode()
            if ch == '\r':
                print("")
                break
            else:
             user_input = user_input + ch
             print(ch, end='', flush=True)
        else:
            ready_to_read, ready_to_write, in_error = select.select([my_socket], [], [], 0.1)
            if my_socket in ready_to_read:
                data = my_socket.recv(1024).decode()
                if data:
                 print("server replied:", data)
    messages_to_send.append((str(user_input)))
    for message in messages_to_send:
            my_socket.send(user_input.encode())
            messages_to_send.remove(message)
    if user_input == 'EXIT\r':
            EXIT = True
my_socket.close()

