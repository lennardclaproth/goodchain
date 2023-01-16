from modules.p2pNetwork.server.ServerConnectionHandler import ServerConnection
import State

class MessageHandler:

    @staticmethod
    def send(type, client, msg):
        server_instance = State.instance(ServerConnection).get_value()
        message = msg.encode(server_instance.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(server_instance.FORMAT)
        send_length += b' ' * (server_instance.HEADER - len(send_length))
        client.send(send_length)
        client.send(message)

    def receive(type, client):
        server_instance = State.instance(ServerConnection).get_value()
        return client.recv(2048).decode(server_instance.FORMAT)