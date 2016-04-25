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
        self.assertEqual(class_for_testing.hello, 'world')


def callback_logic(instance, attr_to_set, value_to_set):
    print('Callback called for {}, {}, {}'.format(instance, attr_to_set, value_to_set))
    setattr(instance, attr_to_set, value_to_set)


@retry_decorator.retry(ExceptionToCheck=AttributeError, tries=2, callback_by_exception={
    AttributeError: functools.partial(callback_logic, class_for_testing, 'hello', 'world')})
def my_test_func():
    x = 3
    print(x.split(','))


if __name__ == '__main__':
    unittest.main()
