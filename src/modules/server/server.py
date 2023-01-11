import select
import socket
import threading
from modules.logging.Logger import Logger

class Server:

    def __init__(self):
        self.IP_ADDR = socket.gethostbyname(socket.gethostname())
        self.PORT = 5050
        self.HEADER = 64
        self.FORMAT = 'utf-8'
        self.SERVER_INSTANCE = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SERVER_INSTANCE.bind((self.IP_ADDR,self.PORT))
        server_thread = threading.Thread(target=self.server_start, args=())
        server_thread.start()

    def server_start(self):
        self.SERVER_INSTANCE.listen()
        Logger.log("SERVER", "STARTED", f"Server is listening on {self.IP_ADDR}")
        while True:
            conn, addr = self.SERVER_INSTANCE.accept()
            thread = threading.Thread(target=self.client_connection, args=(conn, addr))
            thread.start()

    def p2p_connection():
        #TODO: implement connection_handler to different p2p servers
        Logger.log("SERVER","CONNECT TO PEER","connected to peer connection at peer")
        
    def client_connection(self, conn, addr):
        client_name = conn.recv(2048).decode(self.FORMAT)
        Logger.log("SERVER", "CLIENT CONNECT", f"{addr} >> client connected.")
        connection_message = f"...\nHi {client_name}! \nYou are successfully connected to the server {(self.IP_ADDR,self.PORT)}"
        conn.send(connection_message.encode(self.FORMAT))
        connected = True
        while connected:
            ready_to_read, ready_to_write, in_error = select.select([conn],[],[conn],2000)
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
        bye_message = f"\nBye {client_name}!"
        conn.send(bye_message.encode(self.FORMAT))
        conn.close()
        