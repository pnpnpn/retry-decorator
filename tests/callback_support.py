import unittest
import functools

import retry_decorator


class ClassForTesting(object):
    hello = None


class_for_testing = ClassForTesting()


class MyTestCase(unittest.TestCase):
    def test_something(self):
        try:
            my_test_func()
        except Exception:  # for the dangling exception (the "final" function execution)
            pass
        self.assertIn(class_for_testing.hello, ('world', 'fish', ))

    def test_two_exceptions_to_check_use_one(self):
        try:
            my_test_func_2()
        except Exception:
            pass
        self.assertIn(class_for_testing.hello, ('world', 'fish', ))


def callback_logic(instance, attr_to_set, value_to_set):
    print('Callback called for {}, {}, {}'.format(instance, attr_to_set, value_to_set))
    setattr(instance, attr_to_set, value_to_set)


class TestError(Exception):
    pass


@retry_decorator.retry(ExceptionToCheck=TestError, tries=2, callback_by_exception={
    TestError: functools.partial(callback_logic, class_for_testing, 'hello', 'world')})
def my_test_func():
    raise TestError('oh noes.')


@retry_decorator.retry(ExceptionToCheck=(TestError, AttributeError), tries=2, callback_by_exception={
    AttributeError: functools.partial(callback_logic, class_for_testing, 'hello', 'fish')})
def my_test_func_2():
    raise AttributeError('attribute oh noes.')

if __name__ == '__main__':
    unittest.main()
