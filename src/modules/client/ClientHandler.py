import select
import socket
import threading
import time
import State
from modules.logging.Logger import Logger
from modules.server.Server import Server
class Client:

    def __init__(self):
        self.IP_ADDR = State.instance(Server).get_value().IP_ADDR
        self.SERVER_PORT = State.instance(Server).get_value().PORT
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
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(2)
        ADDR = (f'192.168.64.{ip}', self.SERVER_PORT)
        try:
            client.connect(ADDR)
            # Logger.log("CLIENT","CONNECTED MESSAGE", f"connected to: {ADDR}, message from server: {client.recv(2048).decode(self.FORMAT)}")
            # connected = True
            # while connected:
                # ready_to_write, ready_to_read, on_error = select.select([client],[client],[client])
            self.send(client, "test string")
            # self.send(client, "!DISCONNECT")
                # connected = False
            client.close()
        except OSError:
            return
        except Exception as e:
            Logger.log("SERVER", "ERROR", f"An error occured while trying to broadcast to IP:192.168.64.{i} nested exception is {e}")

    def send(self, client, msg):
        message = msg.encode(self.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        client.send(send_length)
        client.send(message)