import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
hostname=socket.gethostname()   
HOST_IP=socket.gethostbyname(hostname)
HOST_IP = '192.168.64.6'

ADDR = (HOST_IP, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
client_name = input('please enter your name: ')
client.send(client_name.encode(FORMAT))
print(client.recv(2048).decode(FORMAT))

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

cont_flag = True
while cont_flag:
    print('--------------------------')
    print('You can send a message to server')
    print('to stop connection, press enter on a blank message')
    mes = input('Your message: ')
    if mes:
        send(mes)
    else:
        send(DISCONNECT_MESSAGE)
        cont_flag = False

# class Client:

#     def __init__(self):
        