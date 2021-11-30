import sys
import unittest

sys.path.append('./')
import common.variables as variables
from common.utils import *
from common.variables import *


class UnitTestUtils(unittest.TestCase):
    test_message = {'action': 'presence',
                    'time': 'Sat Nov  6 18:29:04 2021',
                    'user': {'account_name': 'Guest'}}

    def test_check_client_sock(self):
        self.assertTrue(client_socket(DEFAULT_IP_ADDRESS, DEFAULT_PORT))


if __name__ == '__main__':
    unittest.main()
