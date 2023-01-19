from hashlib import sha256
import random
import string
import sys
import State
from modules.db.context import DbContext

from modules.signing.Signature import Signature
from modules.user.User import User

from modules.p2pNetwork.messaging.MessageQueue import Task, MessageQueue


class UserContext:
    def __init__(self, dbContext: DbContext):
        self.db_context = dbContext
        self.cursor = dbContext.connection.cursor()
        self.create_table_if_not_exists()

    def create_table_if_not_exists(self):
        statement = 'CREATE TABLE IF NOT EXISTS users (user_id TEXT PRIMARY KEY, username TEXT UNIQUE, password TEXT, private_key TEXT, public_key TEXT)'
        self.cursor.execute(statement)
        self.db_context.connection.commit()

    def create_user(self, username, password):
        private_key, public_key = Signature.generate_keys()
        password_hashed = sha256(password).hexdigest()
        chars = string.ascii_uppercase + string.digits
        user_id = f"{''.join(random.choice(chars) for _ in range(4))}-{''.join(random.choice(chars) for _ in range(4))}-{''.join(random.choice(chars) for _ in range(4))}"
        user = self.cursor.execute("INSERT INTO users (user_id,username,password,private_key,public_key) VALUES (?,?,?,?,?);", (user_id,str(
            username, 'utf-8'), password_hashed, private_key, public_key))
        self.db_context.connection.commit()
        task = Task(("CLIENT","USER_CREATE"), self.find_user(username))
        queue : MessageQueue = State.instance(MessageQueue).get_value()
        queue.lock()
        queue.enqueue(task)
        queue.release()
        return user

    def insert_user(self, user: User):
        user = self.cursor.execute("INSERT INTO users (user_id,username,password,private_key,public_key) VALUES (?,?,?,?,?);", (user.user_id,user.username, user.password, user.private_key, user.public_key))
        return user

    def sync(self, users):
        # TODO: get all users from db
        all_users = []

    def find_user(self, _username):
        try:
            user_id, username, password, private_key, public_key = self.cursor.execute("SELECT * FROM users WHERE username=?", (str(_username,'utf-8'),)).fetchone()
            user = User(user_id, username, password, private_key, public_key)
            return user
        except TypeError as e:
            raise ValueError(f'User not found with username {_username}, query resulted in None.\nNested exception is: {e}')
    
    def find_user_by_pbc(self, _pbc):
        try:
            user_id, username, password, private_key, public_key = self.cursor.execute("SELECT * FROM users WHERE public_key=?", (_pbc,)).fetchone()
            user = User(user_id, username, password, private_key, public_key)
            return user
        except TypeError as e:
            raise ValueError(f'User not found with pbc {_pbc}, query resulted in None.\nNested exception is: {e}')
