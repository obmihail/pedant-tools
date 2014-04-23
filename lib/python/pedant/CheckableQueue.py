import Queue

class CheckableQueue(Queue.Queue):
    def __contains__(self, item):
        with self.mutex:
            return item in self.queue