import unittest
from functools import partial

import retry_decorator


class ClassForTesting(object):
    hello = None
    cb_counter = 0  # counts how many times callback was invoked
    exe_counter = 0  # counts how many times our retriable logic was invoked


class ExampleTestError(Exception):
    pass


class_for_testing = None


class MyTestCase(unittest.TestCase):

    def setUp():
        global class_for_testing
        class_for_testing = ClassForTesting()

    def test_callback_invoked_on_configured_exception_type(self):
        try:
            my_test_func()
        except Exception:  # for the dangling exception (the "final" function execution)
            pass
        self.assertEqual(class_for_testing.hello, 'world')

    def test_two_exceptions_to_check_use_one(self):
        try:
            my_test_func_2()
        except Exception:
            pass
        self.assertEqual(class_for_testing.hello, 'fish')
        self.assertEqual(class_for_testing.cb_counter, 1)
        self.assertEqual(class_for_testing.exe_counter, 2)

    def test_callback_by_exception_may_be_func(self):
        try:
            my_test_func_3()
        except Exception:
            pass
        self.assertEqual(class_for_testing.hello, 'foo')

    def test_callback_by_exception_may_be_tuple(self):
        try:
            my_test_func_4()
        except Exception:
            pass
        self.assertEqual(class_for_testing.hello, 'bar')

    def test_verify_correct_amount_of_retries_and_callback_invokations(self):
        try:
            my_test_func_5()
        except Exception:
            pass
        self.assertEqual(class_for_testing.hello, 'bar')
        self.assertEqual(class_for_testing.cb_counter, 10)
        self.assertEqual(class_for_testing.exe_counter, 6)

    def test_verify_correct_amount_of_retries_and_callback_invokations2(self):
        try:
            my_test_func_6()
        except Exception:
            pass
        self.assertEqual(class_for_testing.hello, 'foo')
        self.assertEqual(class_for_testing.cb_counter, 5)
        self.assertEqual(class_for_testing.exe_counter, 6)

    def test_verify_breakout_true_works(self):
        try:
            my_test_func_7()
        except Exception:
            pass
        self.assertEqual(class_for_testing.hello, 'baz')
        self.assertEqual(class_for_testing.cb_counter, 6)
        self.assertEqual(class_for_testing.exe_counter, 7)

    def test_verify_run_last_time_false_works(self):
        try:
            my_test_func_8()
        except Exception:
            pass
        self.assertEqual(class_for_testing.hello, 'bar')
        self.assertEqual(class_for_testing.cb_counter, 14)
        self.assertEqual(class_for_testing.exe_counter, 7)  # note value is tries-1 because of run_one_last_time=False


def callback_logic(instance, attr_to_set, value_to_set):
    print('Callback called for {}; setting attr [{}] to value [{}]'.format(instance, attr_to_set, value_to_set))
    setattr(instance, attr_to_set, value_to_set)
    instance.cb_counter += 1


def get_callback_tuple_breakout(attr_value, breakout_value=False):
    return (partial(callback_logic, class_for_testing, 'hello', attr_value), breakout_value)


@retry_decorator.retry(exc=ExampleTestError, tries=2, callback_by_exception={
    ExampleTestError: partial(callback_logic, class_for_testing, 'hello', 'world')})
def my_test_func():
    raise ExampleTestError('oh noes.')


@retry_decorator.retry(exc=(ExampleTestError, AttributeError), tries=2, callback_by_exception={
    AttributeError: partial(callback_logic, class_for_testing, 'hello', 'fish')})
def my_test_func_2():
    class_for_testing.exe_counter += 1
    raise AttributeError('attribute oh noes.')


@retry_decorator.retry(tries=2, callback_by_exception=partial(callback_logic, class_for_testing, 'hello', 'foo'))
def my_test_func_3():
    raise TypeError('type oh noes.')


@retry_decorator.retry(tries=2, callback_by_exception=(partial(callback_logic, class_for_testing, 'hello', 'bar'), False))
def my_test_func_4():
    raise TypeError('type oh noes.')


@retry_decorator.retry(tries=6, callback_by_exception={
    TypeError: partial(callback_logic, class_for_testing, 'hello', 'foo'),
    Exception: partial(callback_logic, class_for_testing, 'hello', 'bar')
    })
def my_test_func_5():
    class_for_testing.exe_counter += 1
    raise TypeError('type oh noes.')


@retry_decorator.retry(exc=ExampleTestError, tries=6, callback_by_exception={
    TypeError: partial(callback_logic, class_for_testing, 'hello', 'bar'),
    ExampleTestError: partial(callback_logic, class_for_testing, 'hello', 'foo')
    })
def my_test_func_6():
    class_for_testing.exe_counter += 1
    raise ExampleTestError('oh noes.')


@retry_decorator.retry(tries=7, callback_by_exception={
    TypeError: (partial(callback_logic, class_for_testing, 'hello', 'baz'), True),
    Exception: partial(callback_logic, class_for_testing, 'hello', 'foo')
    })
def my_test_func_7():
    class_for_testing.exe_counter += 1
    raise TypeError('type oh noes.')


@retry_decorator.retry(tries=8, callback_by_exception={
    TypeError: partial(callback_logic, class_for_testing, 'hello', 'foo'),
    Exception: (partial(callback_logic, class_for_testing, 'hello', 'bar'), False, False)
    })
def my_test_func_8():
    class_for_testing.exe_counter += 1
    raise TypeError('type oh noes.')


if __name__ == '__main__':
    unittest.main()
