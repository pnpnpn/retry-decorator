#!/usr/bin/env python

#
# License: MIT
# Copyright: Patrick Ng - 2012
#

from __future__ import print_function
from retry_decorator import *


@retry(Exception, tries=3, timeout_secs=0.1)
def retry_test():
    import sys
    print('hello', file=sys.stderr)
    raise Exception('Testing retry')

if __name__ == '__main__':
    try:
        retry_test()
    except Exception as e:
        print('Received the last exception')
