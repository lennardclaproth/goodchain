import select
import socket
import threading
import time
import State
from modules.p2pNetwork.messaging.Handler import ClientMessageHandler, MessageHandler
from modules.p2pNetwork.Logging import Logger
from modules.p2pNetwork.server.ServerConnectionHandler import ServerConnection
class ClientConnection:

    def __init__(self):
        self.IP_ADDR = State.instance(ServerConnection).get_value().IP_ADDR
        self.SERVER_PORT = State.instance(ServerConnection).get_value().PORT
        self.HEADER = 64
        self.FORMAT = 'utf-8'
        try:
            broadcast_thread = threading.Thread(target=self.broadcast, args=())
            broadcast_thread.start()
        except Exception as e:
            Logger.log("CLIENT", "ERROR", f"An error occured while starting the broadcast thread, nested exception is{e}")

    def broadcast(self):
        while True:
            # State.instance(MessageQueue).get_value()
            own_ip = self.IP_ADDR.split('.')[-1]
            for i in range(1, 255):
                if i is not int(own_ip):
                    connect_thread = threading.Thread(target=self.connect, args=(i,))
                    connect_thread.start()
            time.sleep(10)
            
    def connect(self, ip):
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.settimeout(2)
        ADDR = (f'192.168.64.{ip}', self.SERVER_PORT)
        try:
            conn.connect(ADDR)
            # TODO: connect should be as follow -> connect -> connection accepted server -> send message -> message received -> disconnect
            connected = True
            messageHandler = ClientMessageHandler(conn)
            while connected:
                ready_to_read, ready_to_write, on_error = select.select([conn],[conn],[conn])
                if ready_to_read:
                    messageHandler.receive()
                if ready_to_write:
                    messageHandler.send("test string")

                time.sleep(10)
            conn.close()
        except OSError:
            return
        except Exception as e:
            Logger.log("SERVER", "ERROR", f"An error occured while trying to broadcast to IP:192.168.64.{ip} nested exception is {e}")