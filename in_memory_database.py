
from collections import defaultdict


class InMemoryDatabase:
    def __init__(self):
        self._db = {}
        self._values_count = defaultdict(int)

    def set(self, name, value):
        previous_value = self._db.get(name, None)
        if previous_value:
            self._values_count[previous_value] -= 1
        self._db[name] = value
        self._values_count[value] += 1
    
    def get(self, name):
        return self._db.get(name, None)
    
    def delete(self, name):
        if name in self._db:
            value = self._db[name]
            del self._db[name]
            self._values_count[value] -= 1

    def count(self, value):
        return self._values_count[value]

    def handle(self, request):
        COMMANDS = {
            'SET': self.set,
            'GET': self.get,
            'DELETE': self.delete,
            'COUNT': self.count,
        }
        request = request.split()
        command = COMMANDS[request[0]]
        name = request[1]
        if len(request) == 3:
            value = request[2]
            return command(name, value)
        return command(name)

