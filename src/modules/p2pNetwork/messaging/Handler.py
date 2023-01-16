from modules.p2pNetwork.Logging import Logger
from modules.p2pNetwork.server.ServerConnectionHandler import ServerConnection
import State

class MessageHandler:
    def __init__(self, conn):
        self.conn = conn
        self.HEADER = 64
        self.FORMAT = 'utf-8'
        self.message_received = None
        self.message_sent = None

class ServerMessageHandler (MessageHandler):

    def __init__(self, conn):
        super().__init__(conn)
        self.close_connection_msg = "CLOSE CONNECTION"
        self.message_queue = []
        
    def send(self, msg):
        # server_instance = State.instance(ServerConnection).get_value()
        message = msg.encode(self.FORMAT)
        # msg_length = len(message)
        # send_length = str(msg_length).encode(self.FORMAT)
        # send_length += b' ' * (self.HEADER - len(send_length))
        # self.conn.send(send_length)
        
        Logger.log("SERVER","SEND MESSAGE", f"message sent '{msg}'")
        self.conn.send(message)

    def receive(self):
        # if msg_length:
            # msg_length = int(msg_length)
        msg = self.conn.recv(2048).decode(self.FORMAT)
        if msg == "!DISCONNECT":
            connected = False
        return_message = f'Server received your message: "{msg}"'
        Logger.log("SERVER","RECEIVED MESSAGE", f"message received '{msg}'")
        # self.send(return_message)
        self.conn.send(return_message.encode(self.FORMAT))

class ClientMessageHandler (MessageHandler):

    def __init__(self, conn):
        super().__init__(conn)
        self.close_connection_msg = "CLOSE CONNECTION"
        
    def send(self, msg):
        message = msg.encode(self.FORMAT)
        # msg_length = len(message)
        # send_length = str(msg_length).encode(self.FORMAT)
        # send_length += b' ' * (self.HEADER - len(send_length))
        # self.conn.send(send_length)
        Logger.log("CLIENT","SEND MESSAGE", f"message sent '{msg}'")
        self.conn.send(message)

    def receive(self):
        # msg_length = self.conn.recv(self.HEADER).decode(self.FORMAT)
        # if msg_length:
            # msg_length = int(msg_length)
        msg = self.conn.recv(2048).decode(self.FORMAT)
        return_message = f'Client received message'
        Logger.log("CLIENT","RECEIVED MESSAGE", f"message received '{msg}'")
        # self.conn.send(return_message.encode(self.FORMAT))
        self.conn.send(return_message.encode(self.FORMAT))