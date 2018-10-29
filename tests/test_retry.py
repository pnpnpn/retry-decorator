#!/usr/bin/env python

#
# License: MIT
# Copyright: Patrick Ng - 2012
#
"""Retry decorator tests and test dependencies"""

from __future__ import print_function
import sys
import unittest
import functools
from retry_decorator import retry

sys.tracebacklimit = 0


class RetryTestError(Exception):
    """Custom exception for testing purposes"""
    pass


@retry(RetryTestError, tries=3, timeout_secs=0.1)
def will_retry():
    """Function that retries"""
    raise RetryTestError('Testing retry')


@retry(RetryTestError, RuntimeError, tries=3, timeout_secs=0.1)
def will_retry_two_exceptions():
    """Retry and catch multiple exceptions"""
    raise RetryTestError('Testing retry with multiple exceptions')


@retry(RetryTestError)
def will_raise_something_else():
    """Raises an exception the retry decorator won't catch"""
    raise RuntimeError


@retry(RetryTestError, AssertionError, RuntimeError, KeyError, tries=3,
       timeout_secs=0.1)
def will_retry_four_exceptions():
    """Retry will catch four exceptions"""
    raise RetryTestError


@retry(RetryTestError, RuntimeError, tries=3, timeout_secs=0.1)
def will_retry_second_exception():
    """Retry and catch multiple exceptions"""
    raise RuntimeError('Testing retry with multiple exceptions')


class TestRetry(unittest.TestCase):
    """Unit tests for the retry decorator"""

    def test_retry(self):
        """Test retry decorator throws"""
        self.assertRaises(RetryTestError, will_retry)

    def test_retry_multiple_exceptions(self):
        """Test retry decorator for multiple exceptions"""
        self.assertRaises(RetryTestError, will_retry_two_exceptions)

    def test_retry_four_exceptions(self):
        """Test retry decorator for 4 exceptions"""
        self.assertRaises(RetryTestError, will_retry_four_exceptions)

    def test_retry_wrong_exception(self):
        """Test retry decorator with unexpected error"""
        self.assertRaises(RuntimeError, will_raise_something_else)

    def test_retry_second_exception(self):
        """Test retry decorator for second exception"""
        self.assertRaises(RuntimeError, will_retry_second_exception)


class ClassForTesting(object):
    hello = None


class_for_testing = ClassForTesting()


class TestCallbacks(unittest.TestCase):

    def test_something(self):
        try:
            my_test_func()
        # for the dangling exception (the "final" function execution)
        except RetryTestError:
            pass
        self.assertIn(class_for_testing.hello, ('world', 'fish', ))

    def test_two_exceptions_to_check_use_one(self):
        try:
            my_test_func_2()
        except AttributeError:
            pass
        self.assertIn(class_for_testing.hello, ('world', 'fish', ))


def callback_logic(instance, attr_to_set, value_to_set):
    print('Callback called for {}, {}, {}'.format(instance, attr_to_set, value_to_set))
    setattr(instance, attr_to_set, value_to_set)


@retry(RetryTestError, tries=2, callback_by_exception={
    RetryTestError: functools.partial(callback_logic, class_for_testing, 'hello', 'world')})
def my_test_func():
    raise RetryTestError('oh noes.')


@retry(RetryTestError, AttributeError, tries=2, callback_by_exception={
    AttributeError: functools.partial(callback_logic, class_for_testing, 'hello', 'fish')})
def my_test_func_2():
    raise AttributeError('attribute oh noes.')


if __name__ == '__main__':
    unittest.main(verbosity=2)
