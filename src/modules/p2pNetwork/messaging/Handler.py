from modules.p2pNetwork.Logging import Logger
from modules.p2pNetwork.server.ServerConnectionHandler import ServerConnection
import State

# TODO: change to 1 message handler (divide between SERVER and CLIENT and set initial message state)
# TODO: implment message_queue in the message handler
# TODO: connect should be as follow -> connect -> connection accepted server -> send message -> message received -> disconnect


class MessageHandler:
    def __init__(self, conn, type, initial_state):
        self.conn = conn
        self.HEADER = 64
        self.FORMAT = 'utf-8'
        self.type = type
        self.initial_state = initial_state
        self.message_received = None
        self.message_sent = None

    def send(self, msg):
        message = msg.encode(self.FORMAT)
        Logger.log(self.type, "SEND MESSAGE", f"message @{self.conn.getpeername()}: '{msg}'")
        self.conn.send(message)

    def receive(self, msg):
        msg = self.conn.recv(2048).decode(self.FORMAT)
        return_message = f'Server received your message: "{msg}"'
        Logger.log(self.type, "RECEIVED MESSAGE", f"message @{self.conn.getpeername()}: '{msg}'")
        # self.message_queue.append(return_message)s

# class ServerMessageHandler (MessageHandler):

#     def __init__(self, conn):
#         super().__init__(conn)
#         self.close_connection_msg = "CLOSE CONNECTION"
#         self.message_queue = []
        
#     def send(self, msg):
#         # server_instance = State.instance(ServerConnection).get_value()
#         message = msg.encode(self.FORMAT)
#         # msg_length = len(message)
#         # send_length = str(msg_length).encode(self.FORMAT)
#         # send_length += b' ' * (self.HEADER - len(send_length))
#         # self.conn.send(send_length)
        
#         Logger.log("SERVER","SEND MESSAGE", f"message sent '{msg}'")
#         self.conn.send(message)

#     def receive(self):
#         # if msg_length:
#             # msg_length = int(msg_length)
#         msg = self.conn.recv(2048).decode(self.FORMAT)
#         return_message = f'Server received your message: "{msg}"'
#         Logger.log("SERVER","RECEIVED MESSAGE", f"message received '{msg}'")
#         self.message_queue.append(return_message)
#         # self.send(return_message)
#         # self.conn.send(return_message.encode(self.FORMAT))

# class ClientMessageHandler (MessageHandler):

#     def __init__(self, conn):
#         super().__init__(conn)
#         message_queue = [("REQUEST CONNECTION", f"Client requesting connection to server @{self.conn.getpeername()}")]
        
#     def send(self, msg):
#         message = msg.encode(self.FORMAT)
#         # msg_length = len(message)
#         # send_length = str(msg_length).encode(self.FORMAT)
#         # send_length += b' ' * (self.HEADER - len(send_length))
#         # self.conn.send(send_length)
#         Logger.log("CLIENT","SEND MESSAGE", f"message sent to server {self.conn.getpeername()}'{msg}'")
#         self.conn.send(message)

#     def receive(self):
#         # msg_length = self.conn.recv(self.HEADER).decode(self.FORMAT)
#         # if msg_length:
#             # msg_length = int(msg_length)
#         msg = self.conn.recv(2048).decode(self.FORMAT)
#         return_message = f'Client received message'
#         Logger.log("CLIENT","RECEIVED MESSAGE", f"message received '{msg}'")
#         # self.conn.send(return_message.encode(self.FORMAT))
#         # self.conn.send(return_message.encode(self.fo))