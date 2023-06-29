
from collections import defaultdict, deque

class Transaction:
    def __init__(self):
        self._rollback_instructions = []

    def add_rollback_instruction(self, instruction):
        self._rollback_instructions.append(instruction)

    def rollback(self):
        for instruction in self._rollback_instructions:
            instruction()


class InMemoryDatabase:
    def __init__(self):
        self._db = {}
        self._values_count = defaultdict(int)
        self._transactions = []

    def set(self, name, value):
        previous_value = self._db.get(name, None)
        if previous_value:
            self._values_count[previous_value] -= 1
        self._db[name] = value
        self._values_count[value] += 1
        
        if self._transactions:
            current_transaction = self._transactions[-1]
            if previous_value:
                current_transaction.add_rollback_instruction(lambda: self.set(name, previous_value))
            else:
                current_transaction.add_rollback_instruction(lambda: self.delete(name))
    
    def get(self, name):
        return self._db.get(name, None)
    
    def delete(self, name):
        if self._transactions:
            current_transaction = self._transactions[-1]
            current_transaction.add_rollback_instruction(lambda: self.set(name, self._db[name]))

        if name in self._db:
            value = self._db[name]
            del self._db[name]
            self._values_count[value] -= 1

    def count(self, value):
        return self._values_count[value]
    
    def begin(self):
        self._transactions.append(Transaction())

    def rollback(self):
        if not self._transactions:
            return 'NO TRANSACTION'
        self._transactions.pop().rollback()


    def commit(self):
        if not self._transactions:
            return 'NO TRANSACTION'
        self._transactions = []
            

    def handle(self, request):
        COMMANDS = {
            'SET': self.set,
            'GET': self.get,
            'DELETE': self.delete,
            'COUNT': self.count,
            'BEGIN': self.begin,
            'ROLLBACK': self.rollback,
            'COMMIT': self.commit,
        }
        request = request.split()
        command = COMMANDS[request[0]]
        if len(request) == 1:
            return command()
        
        name = request[1]
        if len(request) == 2:
            return command(name)
        
        value = request[2]
        return command(name, value)
        

