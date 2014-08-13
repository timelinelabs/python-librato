import logging
import unittest
import librato
from mock_connection import MockConnect, server

#logging.basicConfig(level=logging.DEBUG)
# Mock the server
librato.HTTPSConnection = MockConnect

class TestLibratoAlerts(unittest.TestCase):
	def setUp(self):
		self.conn = librato.connect('user_test', 'key_test')
		server.clean()

if __name__ == '__main__':
    unittest.main()