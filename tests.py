
from collections import namedtuple
from in_memory_database import InMemoryDatabase
import unittest

TestRequest = namedtuple('TestRequest', ['request', 'expected_output'])

class Tests(unittest.TestCase):
    def _run_test(self, test_requests):
        db = InMemoryDatabase()
        for i, test_request in enumerate(test_requests):
            self.assertEqual(db.handle(test_request.request), test_request.expected_output, f"request-{i + 1}: {test_request}")

    def test_standard1(self):
        requests = [
            TestRequest('SET a 10', None),
            TestRequest('GET a', '10'),
            TestRequest('DELETE a', None),
            TestRequest('GET a', None),
        ]
        self._run_test(requests)
    
    def test_standard2(self):
        requests = [
            TestRequest('SET a 10', None),
            TestRequest('SET a 20', None),
            TestRequest('GET a', '20'),
            TestRequest('DELETE a', None),
            TestRequest('GET a', None),
        ]
        self._run_test(requests)
    
    def test_standard3(self):
        requests = [
            TestRequest('SET a 10', None),
            TestRequest('SET b 10', None),
            TestRequest('COUNT 10', 2),
            TestRequest('COUNT 20', 0),
            TestRequest('DELETE a', None),
            TestRequest('COUNT 10', 1),
            TestRequest('SET b 30', None),
            TestRequest('COUNT 10', 0),
        ]
        self._run_test(requests)

    def test_transactions1(self):
        requests = [
            TestRequest('BEGIN', None),
            TestRequest('SET a 10', None),
            TestRequest('GET a', '10'),
            TestRequest('BEGIN', None),
            TestRequest('SET a 20', None),
            TestRequest('GET a', '20'),
            TestRequest('ROLLBACK', None),
            TestRequest('GET a', '10'),
            TestRequest('ROLLBACK', None),
            TestRequest('GET a', None),
        ]

        self._run_test(requests)

    def test_transactions2(self):
        requests = [
            TestRequest('BEGIN', None),
            TestRequest('SET a 30', None),
            TestRequest('BEGIN', None),
            TestRequest('SET a 40', None),
            TestRequest('COMMIT', None),
            TestRequest('GET a', '40'),
            TestRequest('ROLLBACK', 'NO TRANSACTION'),
        ]

        self._run_test(requests)

    def test_transactions3(self):
        requests = [
            TestRequest('SET a 50', None),
            TestRequest('BEGIN', None),
            TestRequest('GET a', '50'),
            TestRequest('SET a 60', None),
            TestRequest('BEGIN', None),
            TestRequest('DELETE a', None),
            TestRequest('GET a', None),
            TestRequest('ROLLBACK', None),
            TestRequest('GET a', '60'),
            TestRequest('COMMIT', None),
            TestRequest('GET a', '60'),

        ]

        self._run_test(requests)

    def test_transactions4(self):
        requests = [
            TestRequest('SET a 10', None),
            TestRequest('BEGIN', None),
            TestRequest('COUNT 10', 1),
            TestRequest('BEGIN', None),
            TestRequest('DELETE a', None),
            TestRequest('COUNT 10', 0),
            TestRequest('ROLLBACK', None),
            TestRequest('COUNT 10', 1),
        ]