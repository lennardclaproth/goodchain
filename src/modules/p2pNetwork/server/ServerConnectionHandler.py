import select
import socket
import threading
from modules.p2pNetwork.Logging import Logger

class ServerConnection:

    def __init__(self):
        self.IP_ADDR = ''
        self.PORT = 5050
        self.SERVER_INSTANCE = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.allocate_ip()
            server_thread = threading.Thread(target=self.server_start, args=())
            server_thread.start()
        except Exception as e:
            Logger.log("SERVER", "ERROR", f"An error occured while starting the server nested exception is{e}")

    def allocate_ip(self):
        for i in range(1, 255):
            try:
                Logger.log("SERVER", "ASSIGN ADDRESS", f"Trying to bind ip 192.168.64.{i}")
                self.SERVER_INSTANCE.bind((f'192.168.64.{i}',self.PORT))
                self.IP_ADDR = f'192.168.64.{i}'
                break
            except OSError:
                continue
            except Exception as e:
                Logger.log("SERVER", "ERROR", f"An error occured while starting the server nested exception is{e}")
        

    def server_start(self):
        try:
            self.SERVER_INSTANCE.listen()
            Logger.log("SERVER", "STARTED", f"Server is listening on {self.IP_ADDR}")
        except Exception as e:
            Logger.log("SERVER", "ERROR", f"An error occured while starting the server nested exception is{e}")
        while True:
            conn, addr = self.SERVER_INSTANCE.accept()
            thread = threading.Thread(target=self.client_connection, args=(conn, addr))
            thread.start()

    # def send(self, client, msg):
    #     message = msg.encode(self.FORMAT)
    #     msg_length = len(message)
    #     send_length = str(msg_length).encode(self.FORMAT)
    #     send_length += b' ' * (self.HEADER - len(send_length))
    #     client.send(send_length)
    #     client.send(message)
        
    def client_connection(self, conn, addr):
        from modules.p2pNetwork.messaging.Handler import ServerMessageHandler
        Logger.log("SERVER", "CLIENT CONNECT", f"{addr} >> client connected.")
        connected = True
        messageHandler = ServerMessageHandler(conn)
        while connected:
            ready_to_read, ready_to_write, in_error = select.select([conn],[conn],[conn],2000)
            # if(len(ready_to_write)):
            #     connection_message = f"You are successfully connected to the server {(self.IP_ADDR,self.PORT)}"
            #     conn.send(connection_message.encode(self.FORMAT))
            if (len(ready_to_write)):
                try:
                    messageHandler.send("test from server")
                except Exception as e:
                    raise e
            if(len(ready_to_read)):
                try:
                    messageHandler.receive()
                except Exception as e:
                    raise e
                # try:
                #     msg_length = conn.recv(self.HEADER).decode(self.FORMAT)
                #     if msg_length:
                #         msg_length = int(msg_length)
                #         msg = conn.recv(msg_length).decode(self.FORMAT)
                #         if msg == "!DISCONNECT":
                #             connected = False

                #         Logger.log("SERVER","CLIENT MESSAGE",f"{addr} >> {msg}")
                #         return_message = f'Server received your message: "{msg}"'
                #         conn.send(return_message.encode(self.FORMAT))
                #     else:
                #         connected = False
                #         # Logger.log("SERVER", "CLIENT DISCONNECT", f"{addr} >> message empty.")
                except ConnectionResetError:
                    connected = False
                    Logger.log("SERVER ERROR", "CLIENT DISCONNECT", f"{addr} >> connection reset by peer.")
            # TODO disconnect
        Logger.log("SERVER", "CLIENT DISCONNECT", f"{addr} >> client disconnected.")
        conn.close()
        