#!/usr/bin/env python

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division

import traceback
import logging
import time
import random

def retry(ExceptionToCheck, tries=10, timeout_secs=1.0, logger=None):
    """
    Retry calling the decorated function using an exponential backoff.
    """
    def deco_retry(f):
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, timeout_secs
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck as e:
                    #traceback.print_exc()
                    half_interval = mdelay * 0.10 #interval size
                    actual_delay = random.uniform(mdelay - half_interval, mdelay + half_interval)
                    msg = "Retrying in %.2f seconds ..." % actual_delay
                    if logger:
                        logger.exception(msg)
                    else:
                        logging.exception(msg)
                    time.sleep(actual_delay)
                    mtries -= 1
                    mdelay *= 2
            return f(*args, **kwargs)
        return f_retry  # true decorator
    return deco_retry

@retry(Exception, tries = 3, timeout_secs = 0.1)
def test_retry():
    import sys
    print('hello', file = sys.stderr)
    raise Exception('Testing retry')

if __name__ == '__main__':
    try:
        test_retry()
    except Exception as e:
        print('Received the last exception')



