import select
import socket
import threading
import ipaddress
from modules.logging.Logger import Logger

# HEADER = 64
# PORT = 5050
# local_ip = socket.gethostbyname(socket.gethostname())
# ADDR = (local_ip, PORT)
# FORMAT = 'utf-8'
# DISCONNECT_MESSAGE = "!DISCONNECT"

# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind(ADDR)

# def handle_client(conn, addr):
#     client_name = conn.recv(2048).decode(FORMAT)

#     print(f"\n[NEW CONNECTION] {client_name}@{addr} is connected.")
#     connection_message = f"...\nHi {client_name}! \nYou are successfully connected to the server {ADDR}"
#     conn.send(connection_message.encode(FORMAT))
#     connected = True
#     while connected:
#         ready_to_read, ready_to_write, in_error = select.select([conn],[],[conn],20)
#         # TODO checkif ready to read

#         if(len(ready_to_read)):
#             msg_length = conn.recv(HEADER).decode(FORMAT)
#             if msg_length:
#                 msg_length = int(msg_length)
#                 msg = conn.recv(msg_length).decode(FORMAT)
#                 if msg == DISCONNECT_MESSAGE:
#                     connected = False

#                 print(f"[{client_name}@{addr}]>> {msg}")
#                 return_message = f'Server received your message: "{msg}"'
#                 conn.send(return_message.encode(FORMAT))
#         # TODO disconnect
    
#     bye_message = f"\nBye {client_name}!"
#     conn.send(bye_message.encode(FORMAT))
#     conn.close()
#     print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}")    

# def start():
#     server.listen()
#     print(f"[LISTENING] Server is listening on {local_ip}")
#     while True:
#         conn, addr = server.accept()
#         thread = threading.Thread(target=handle_client, args=(conn, addr))
#         thread.start()
#         print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


# print("[STARTING] server is starting...")
# start()

class Server:

    def __init__(self):
        self.IP_ADDR = socket.gethostbyname(socket.gethostname())
        # if not self.IP_ADDR.__contains__('192'):
        #     self.IP_ADDR
        self.PORT = 5050
        self.HEADER = 64
        self.FORMAT = 'utf-8'
        self.SERVER_INSTANCE = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SERVER_INSTANCE.bind((self.IP_ADDR,self.PORT))
        thread = threading.Thread(target=self.start, args=())
        thread.start()

    def start(self):
        self.SERVER_INSTANCE.listen()
        # Logger.log()
        Logger.log("SERVER", "STARTED", f"Server is listening on {self.IP_ADDR}")
        # print(f"[LISTENING] Server is listening on {local_ip}")
        while True:
            conn, addr = self.SERVER_INSTANCE.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()

    def handle_client(self, conn, addr):
        client_name = conn.recv(2048).decode(self.FORMAT)
        Logger.log("SERVER", "NEW CONNECTION", f"{client_name}@{addr} is connected.")
        connection_message = f"...\nHi {client_name}! \nYou are successfully connected to the server {ADDR}"
        conn.send(connection_message.encode(self.FORMAT))
        connected = True
        while connected:
            ready_to_read, ready_to_write, in_error = select.select([conn],[],[conn],20)
            # TODO checkif ready to read

            if(len(ready_to_read)):
                msg_length = conn.recv(self.HEADER).decode(self.FORMAT)
                if msg_length:
                    msg_length = int(msg_length)
                    msg = conn.recv(msg_length).decode(self.FORMAT)
                    if msg == "!DISCONNECT":
                        connected = False

                    print(f"[{client_name}@{addr}]>> {msg}")
                    return_message = f'Server received your message: "{msg}"'
                    conn.send(return_message.encode(self.FORMAT))
            # TODO disconnect
        
        bye_message = f"\nBye {client_name}!"
        conn.send(bye_message.encode(self.FORMAT))
        conn.close()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}")