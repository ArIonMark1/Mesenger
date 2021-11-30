import unittest


def rec_method(numb, even=0, odd=0):
    if numb == 0:  # базовое значение
        return even, odd  # возврат значений щетчика если условие верно

    else:
        last_n = numb % 10  # берем последний элемент числа
        numb = numb // 10  # удаляем из числа последний элемент
        if last_n % 2 == 0:  # проверка взятого элемента( четный или не четный)
            even += 1
            return rec_method(numb, even, odd)
        else:
            odd += 1
            return rec_method(numb, even, odd)


# print(rec_method(0))
# print(f"Your number have '{rec_method(123)[0]}' even elements and '{rec_method(123)[1]}' odd elements")


# ==============================
class MyTests(unittest.TestCase):

    def test_check_correct_enter(self):
        self.assertIsInstance(rec_method(444), tuple)

    def test_is_not_in(self):
        self.assertNotIn('some', rec_method(123))

    def test_is_in(self):
        self.assertIn(2, rec_method(123))

    def test_is_true(self):
        self.assertTrue(rec_method(0))


if __name__ == '__main__':
    unittest.main()
