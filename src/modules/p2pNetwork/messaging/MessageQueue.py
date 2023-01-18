import random
import string


class Task:
    def __init__(self, action, data):
        chars = string.ascii_uppercase + string.digits
        self.action = action
        self.id = f"{''.join(random.choice(chars) for _ in range(4))}-{''.join(random.choice(chars) for _ in range(4))}-{''.join(random.choice(chars) for _ in range(4))}"
        self.processed = False
        self.data = data

class MessageQueue:

    def __init__(self):
        self.queue = []
        self.locked = False
        self.message_index = 0

    def enqueue(self, task : Task):
        self.queue.append(task)

    def dequeue(self):
        if self.locked:
            return
        self.queue.pop(0)

    def peek(self):
        if self.locked:
            return None
        if len(self.queue) == 0:
            return None
        return self.queue[0]

    def process(self):
        if self.locked:
            return
        task = self.queue[0]
        task.processed = True
        self.dequeue()

    def lock(self):
        self.locked = True

    def release(self):
        self.locked = False