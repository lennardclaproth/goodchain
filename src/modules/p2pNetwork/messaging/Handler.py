from modules.p2pNetwork.Logging import Logger
from modules.p2pNetwork.server.ServerConnectionHandler import ServerConnection

# TODO: change to 1 message handler (divide between SERVER and CLIENT and set initial message state)
# TODO: implment message_queue in the message handler
# TODO: connect should be as follow -> connect -> connection accepted server -> send message -> message received -> disconnect

class MessageHandler:
    def __init__(self, conn, type, initial_state):
        client = ["CONNECT", "ACTION", "DISCONNECT"]
        server = ["ACCEPT", "RECEIVED"]
        if type == "SERVER":
            self.message_flow_receive = client
            self.message_flow_send = server
        else:
            self.message_flow_send = client
            self.message_flow_receive = server
        self.message_flow_index = 0
        self.conn = conn
        self.HEADER = 64
        self.FORMAT = 'utf-8'
        self.type = type
        self.initial_state = initial_state
        self.message_received = None
        self.message_sent = None
        
    def send(self):
        message = self.message_flow_send[self.message_flow_index]
        Logger.log(self.type, "SEND MESSAGE", f"message @{self.conn.getpeername()}: '{message}'")
        message = message.encode(self.FORMAT)
        self.conn.send(message)

    def receive(self):
        msg = self.conn.recv(2048).decode(self.FORMAT)
        # self.message_flow_index = self.message_flow_receive.index(msg)
        Logger.log(self.type, "RECEIVED MESSAGE", f"message @{self.conn.getpeername()}: '{msg}'")
        self.message_flow_index += 1