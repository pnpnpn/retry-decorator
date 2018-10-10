#!/usr/bin/env python

#
# License: MIT
# Copyright: Patrick Ng - 2012
#

from __future__ import print_function
from retry_decorator import retry


@retry(Exception, tries=3, timeout_secs=0.1)
def test_retry():
    import sys
    print('hello', file=sys.stderr)
    raise Exception('Testing retry')

@retry(AttributeError, RuntimeError, tries=3)
def test_multiple_exceptions():
    print('hi')
    raise AttributeError('Testing retry with multiple exceptions')

if __name__ == '__main__':
    try:
        test_retry()
    except Exception as e:
        print('Received the last exception')

    try:
        test_multiple_exceptions()
    except AttributeError:
        print('Received the last exception for multipme exceptions')
