# By Yael Vaisberger 211526462
# 26/11/22
MAX_MSG_LENGTH = 2048


# checks if msg received is valid
def recv_msg(data):
    if data[0:4] == "NAME" or data[0:9] == "GET_NAMES" or data[0:4] == "EXIT" or data[0:3] == "MSG" or data == "":
        return True, data
    return False, data
