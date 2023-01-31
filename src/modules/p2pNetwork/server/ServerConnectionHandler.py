import select
import socket
import threading
from modules.p2pNetwork.Logging import Logger
# from modules.p2pNetwork.messaging.Handler import MessageHandler

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
        
    def client_connection(self, conn, addr):
        from modules.p2pNetwork.messaging.MessageHandler import MessageHandler
        # Logger.log("SERVER", "CLIENT CONNECT", f"{addr} >> client connected.")
        messageHandler = MessageHandler(conn, "SERVER", "CONNECT")
        while messageHandler.connected:
            ready_to_read, ready_to_write, in_error = select.select([conn],[conn],[conn],2000)
            if (len(ready_to_read)):
                try:
                    messageHandler.receive()
                    if messageHandler.connected:
                        messageHandler.send()
                except Exception as e:
                    raise e
        # Logger.log("SERVER", "CLIENT DISCONNECT", f"{addr} >> client disconnected.")
        conn.close()
        