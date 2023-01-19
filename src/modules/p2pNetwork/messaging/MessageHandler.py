import pickle
from modules.p2pNetwork.Logging import Logger
from modules.p2pNetwork.server.ServerConnectionHandler import ServerConnection
from modules.p2pNetwork.messaging.MessageQueue import Task

# TODO: change to 1 message handler (divide between SERVER and CLIENT and set initial message state)
# TODO: implment message_queue in the message handler
# TODO: connect should be as follow -> connect -> connection accepted server -> send message -> message received -> disconnect

class MessageHandler:
    def __init__(self, conn, type, initial_state):
        client = ["CONNECT", "ACTION", "DISCONNECT"]
        server = ["ACCEPT", "RECEIVED",""]
        self.connected = True
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
        
    def send(self, task = None):
        # TODO: implement pickle dump
        message = self.message_flow_send[self.message_flow_index]
        message = message.encode(self.FORMAT)
        Logger.log(self.type, "SEND MESSAGE", f"message @{self.conn.getpeername()}: '{message}'")
        if task is not None:
            message = pickle.dumps(task)
        self.conn.send(message)
        if self.message_flow_receive[self.message_flow_index] == "DISCONNECT":
            self.conn.close()
            self.connected = False
        self.message_flow_index += 1

    def receive(self):
        # TODO implement task handler
        # TODO: implement pickle load object on index ...
        msg = self.conn.recv(4096)
        try:
            msg = self.conn.recv(4096).decode(self.FORMAT)
        except Exception as e:
            task : Task = pickle.loads(msg)
            msg = task.action
            
        Logger.log(self.type, "RECEIVED MESSAGE", f"message @{self.conn.getpeername()}: '{msg}'")
        # self.message_flow_index = self.message_flow_receive.index(msg)
        
        if msg == "DISCONNECT":
            self.conn.close()
            self.connected = False
        # self.message_flow_index += 1