
from collections import namedtuple
from in_memory_database import InMemoryDatabase
import unittest

TestRequest = namedtuple('TestRequest', ['request', 'expected_output'])

class Tests(unittest.TestCase):
    def _run_test(self, test_requests):
        db = InMemoryDatabase()
        for i, test_request in enumerate(test_requests):
            self.assertEqual(db.handle(test_request.request), test_request.expected_output, f"request-{i + 1}: {test_request}")

    def test1(self):
        requests = [
            TestRequest('SET a 10', None),
            TestRequest('GET a', '10'),
            TestRequest('DELETE a', None),
            TestRequest('GET a', None),
        ]
        self._run_test(requests)
    
    def test2(self):
        requests = [
            TestRequest('SET a 10', None),
            TestRequest('SET a 20', None),
            TestRequest('GET a', '20'),
            TestRequest('DELETE a', None),
            TestRequest('GET a', None),
        ]
        self._run_test(requests)
    
    def test3(self):
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