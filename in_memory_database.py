
from collections import defaultdict

import signal
import sys

def sigint_handler(signal, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)


class Transaction:
    def __init__(self):
        self._rollback_instructions = []

    def add_rollback_instruction(self, instruction):
        self._rollback_instructions.append(instruction)

    def rollback(self):
        for instruction in reversed(self._rollback_instructions):
            instruction()


class InMemoryDatabase:
    NO_TRANSACTION_ERROR = 'NO TRANSACTION'
    
    def __init__(self):
        self._db = {}
        self._values_count = defaultdict(int)
        self._transactions = []
    
    def handle(self, request):
        COMMANDS = {
            'SET': self._set,
            'GET': self._get,
            'DELETE': self._delete,
            'COUNT': self._count,
            'BEGIN': self._begin,
            'ROLLBACK': self._rollback,
            'COMMIT': self._commit,
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


    def _set(self, name, value, handle_rollback=True):
        previous_value = self._db.get(name, None)
        if previous_value:
            self._values_count[previous_value] -= 1
        self._db[name] = value
        self._values_count[value] += 1

        if handle_rollback:
            rollback_instruction = lambda: self._set(name, previous_value, handle_rollback=False) if previous_value else self._delete(name, handle_rollback=False)
            self._add_rollback_instruction_if_transaction(rollback_instruction)
        
    def _get(self, name):
        return self._db.get(name, None)
    
    def _delete(self, name, handle_rollback=True):
        if name not in self._db:
            return
        
        value = self._db[name]
        del self._db[name]
        self._values_count[value] -= 1

        if handle_rollback:
            self._add_rollback_instruction_if_transaction(lambda: self._set(name, value, handle_rollback=False))

    def _count(self, value):
        return self._values_count[value]
    
    def _begin(self):
        self._transactions.append(Transaction())

    def _rollback(self):
        if not self._transactions:
            return self.NO_TRANSACTION_ERROR
        self._transactions.pop().rollback()

    def _commit(self):
        if not self._transactions:
            return self.NO_TRANSACTION_ERROR
        self._transactions = []

    def _add_rollback_instruction_if_transaction(self, instruction):
        if self._transactions:
            self._transactions[-1].add_rollback_instruction(instruction)
        


if __name__ == '__main__':
    db = InMemoryDatabase()
    while True:
        request = input()
        output = db.handle(request)
        if output is not None:
            print(output)
