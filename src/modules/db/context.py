import sqlite3


import sqlite3


class DbContext:
    def __init__(self):
        self.connection = sqlite3.connect("data/goodchain.db")
