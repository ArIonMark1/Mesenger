import sys

sys.path.append('./')
from server import *
from common.utils import *
from common.variables import USER, ACTION, TIME, ACCOUNT_NAME, RESPONSE, ERROR, DATA, DEFAULT_PORT, DEFAULT_IP_ADDRESS, \
    MAX_CONNECTIONS, SUCCESS, PRESENCE
import time
import unittest


class UnittestsServer(unittest.TestCase):

    err_dict = {RESPONSE: 400, ERROR: 'Not correct sent message!'}
    ok_dict = {RESPONSE: 200, SUCCESS: 'Welcome Guest!'}

    out_from_client = {
        ACTION: PRESENCE,
        TIME: time.ctime(),
        USER: {ACCOUNT_NAME: ACCOUNT_NAME}
    }

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_check_type_out_message(self):
        x = check_message(dict())
        self.assertEqual(type(x), type(dict()))

    def test_check_wrong_response(self):
        resp = check_message(dict())
        self.assertEqual(resp['response'], 400)

    def test_user_in_response(self):
        self.assertNotEqual(check_message({ACTION: PRESENCE, TIME: '1.1', 'user': {'account_name': 'guest'}}), self.ok_dict)


if __name__ == '__main__':
    unittest.main()
