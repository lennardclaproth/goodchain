import select
import socket
import threading
import time
import State
from modules.p2pNetwork.messaging.MessageHandler import MessageHandler
from modules.p2pNetwork.Logging import Logger
from modules.p2pNetwork.messaging.MessageQueue import MessageQueue, Task
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
        queue : MessageQueue = State.instance(MessageQueue).get_value()
        while True:
            if queue is None:
                continue
            task : Task = queue.peek()
            if task is None:
                continue
            own_ip = self.IP_ADDR.split('.')[-1]
            for i in range(1, 255):
                try:
                    if i is not int(own_ip):
                        connect_thread = threading.Thread(target=self.connect, args=(i,task,))
                        connect_thread.start()
                except Exception as e:
                    continue
            queue.process()
            
    def connect(self, ip, task):
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.settimeout(2)
        ADDR = (f'192.168.64.{ip}', self.SERVER_PORT)
        try:
            conn.connect(ADDR)
            # connected = True
            messageHandler = MessageHandler(conn, "CLIENT", "CONNECT")
            messageHandler.send()
            messageHandler.receive()
            messageHandler.send(task)
            messageHandler.receive()
            messageHandler.send()
            # while messageHandler.connected:
            #     ready_to_read, ready_to_write, on_error = select.select([conn],[conn],[conn])
            #     if ready_to_read:
            #         messageHandler.receive()
            #     if ready_to_write:
            #         messageHandler.send()
                # time.sleep(10)
            # conn.close()
        except OSError:
            return
        except Exception as e:
            Logger.log("SERVER", "ERROR", f"An error occured while trying to broadcast to IP:192.168.64.{ip} nested exception is {e}")