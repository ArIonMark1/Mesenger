import sys
import common.variables

sys.path.append('./')
import unittest
from client import *
from common.variables import *
from common.utils import *


class TestClass(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # test 1
    def test_type_out_message(self):
        out = create_presence()
        self.assertIsInstance(out, type(dict()))

    # test 2
    def test_check_answer(self):
        self.assertEqual(process_ans({RESPONSE: 200, SUCCESS: 'Welcome Guest!'}), '200, Welcome Guest!')

    # test 3
    def test_answer_not_equal(self):
        self.assertNotEqual(process_ans({RESPONSE: 400, ERROR: 'Not correct sent message!'}), '200, Welcome Guest!')


if __name__ == '__main__':
    unittest.main()
