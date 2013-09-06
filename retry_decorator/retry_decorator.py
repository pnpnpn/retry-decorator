#!/usr/bin/env python

from __future__ import print_function

import traceback
import logging
import time
import random
import sys

def retry(ExceptionToCheck, tries=10, timeout_secs=1.0, fptr=sys.stderr):
    """
    Retry calling the decorated function using an exponential backoff.
    """
    def deco_retry(f):
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, timeout_secs
            while mtries > 0:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck as e:
                    #traceback.print_exc()
                    half_interval = mdelay * 0.10 #interval size
                    actual_delay = random.uniform(mdelay - half_interval, mdelay + half_interval)
                    msg = "Retrying in %.2f seconds ..." % actual_delay
                    print(msg, file=fptr)
                    time.sleep(actual_delay)
                    mtries -= 1
                    mdelay *= 2
            return f(*args, **kwargs)
        return f_retry  # true decorator
    return deco_retry


