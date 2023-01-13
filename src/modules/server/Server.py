import select
import socket
import threading
import time
from modules.logging.Logger import Logger

class Server:

    def __init__(self):
        if socket.gethostbyname(socket.gethostname()).__contains__('192.168.64'):
            self.IP_ADDR = socket.gethostbyname(socket.gethostname())
        else:
            self.IP_ADDR = '192.168.64.1'
        self.PORT = 5050
        self.HEADER = 64
        self.FORMAT = 'utf-8'
        self.SERVER_INSTANCE = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.SERVER_INSTANCE.bind((self.IP_ADDR,self.PORT))
        except Exception as e:
            Logger.log("SERVER", "ERROR", f"An error occured while starting the server nested exception is{e}")
        server_thread = threading.Thread(target=self.server_start, args=())
        server_thread.start()
        broadcast_thread = threading.Thread(target=self.broadcast, args=())
        broadcast_thread.start()

    def server_start(self):
        
        # TODO: check if discoverable ip already in connected ip's
        # TODO: connect if not
        try:
            self.SERVER_INSTANCE.listen()
            Logger.log("SERVER", "STARTED", f"Server is listening on {self.IP_ADDR}")
        except Exception as e:
            Logger.log("SERVER", "ERROR", f"An error occured while starting the server nested exception is{e}")
        while True:
            conn, addr = self.SERVER_INSTANCE.accept()
            thread = threading.Thread(target=self.client_connection, args=(conn, addr))
            thread.start()

    def broadcast(self):
    #       TODO: implement connection_handler to different p2p servers
    #       TODO: loop through all possible ips in range 192.168.68.1 -> 255
    #       TODO: implement actionQueue
    #       TODO: make connection pool
    #     while True:
    #         # Logger.log("SERVER","CONNECT TO PEER","connected to peer connection at peer")
        while True:
            own_ip = self.IP_ADDR.split('.')[-1]
            i = 1
            for i in range(1, 255):
                if i is not int(own_ip):
                    ADDR = (f'192.168.64.{i}', self.PORT)
                    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    try:
                        client.connect(ADDR)
                        client.send("client_name".encode(self.FORMAT))
                        client.send("!DISCONNECT".encode(self.FORMAT))
                    except Exception as e:
                        Logger.log("SERVER", "ERROR", f"An error occured while trying to broadcast nested exception is {e}")
                    finally:
                        continue
            time.sleep(10)

    def send_message(self):
        server = socket.socket()
        
    def client_connection(self, conn, addr):
        client_name = conn.recv(2048).decode(self.FORMAT)
        Logger.log("SERVER", "CLIENT CONNECT", f"{addr} >> client connected.")
        connected = True
        while connected:
            ready_to_read, ready_to_write, in_error = select.select([conn],[conn],[conn],2000)
            if(len(ready_to_write)):
                connection_message = f"...\nHi {client_name}! \nYou are successfully connected to the server {(self.IP_ADDR,self.PORT)}"
                conn.send(connection_message.encode(self.FORMAT))
            if(len(ready_to_read)):
                try:
                    msg_length = conn.recv(self.HEADER).decode(self.FORMAT)
                    if msg_length:
                        msg_length = int(msg_length)
                        msg = conn.recv(msg_length).decode(self.FORMAT)
                        if msg == "!DISCONNECT":
                            connected = False

                        Logger.log("SERVER","CLIENT MESSAGE",f"{addr} >> {msg}")
                        return_message = f'Server received your message: "{msg}"'
                        conn.send(return_message.encode(self.FORMAT))
                    else:
                        connected = False
                        Logger.log("SERVER", "CLIENT DISCONNECT", f"{addr} >> message empty.")
                except ConnectionResetError:
                    connected = False
                    Logger.log("SERVER ERROR", "CLIENT DISCONNECT", f"{addr} >> connection reset by peer.")
            # TODO disconnect
        Logger.log("SERVER", "CLIENT DISCONNECT", f"{addr} >> client disconnected.")
        conn.close()
        