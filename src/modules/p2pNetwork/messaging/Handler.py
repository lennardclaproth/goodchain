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
        super.__init__(self, conn)
        self.close_connection_msg = "CLOSE CONNECTION"
        
    def send(self, msg):
        server_instance = State.instance(ServerConnection).get_value()
        message = msg.encode(server_instance.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(server_instance.FORMAT)
        send_length += b' ' * (server_instance.HEADER - len(send_length))
        self.conn.send(send_length)
        self.conn.send(message)

    def receive(self):
        msg_length = self.conn.recv(self.HEADER).decode(self.FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = self.conn.recv(msg_length).decode(self.FORMAT)
            if msg == "!DISCONNECT":
                connected = False

            Logger.log("SERVER","CLIENT MESSAGE",f"{addr} >> {msg}")
            return_message = f'Server received your message: "{msg}"'
            self.conn.send(return_message.encode(self.FORMAT))