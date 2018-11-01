#
# License: MIT
# Copyright: Patrick Ng - 2012
#

from __future__ import print_function

import traceback
import logging
import time
import random
import sys


def retry(ExceptionToCheck, tries=10, timeout_secs=1.0, logger=None, callback_by_exception=None):
    """
    Retry calling the decorated function using an exponential backoff.
    :param callback_by_exception: callback/method invocation on certain exceptions
    :type callback_by_exception: None or dict
    """
    def deco_retry(f):
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, timeout_secs
            run_one_last_time = True
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck as e:
                    # check if this exception is something the caller wants special handling for
                    callback_errors = callback_by_exception or {}
                    for error_type in callback_errors:
                        if isinstance(e, error_type):
                            callback_logic = callback_by_exception[error_type]
                            should_break_out = run_one_last_time = False
                            if isinstance(callback_logic, (list, tuple)):
                                callback_logic, should_break_out = callback_logic
                                if isinstance(should_break_out, (list, tuple)):
                                    should_break_out, run_one_last_time = should_break_out
                            callback_logic()
                            if should_break_out:  # caller requests we stop handling this exception
                                break
                    # traceback.print_exc()
                    half_interval = mdelay * 0.10  # interval size
                    actual_delay = random.uniform(mdelay - half_interval, mdelay + half_interval)
                    msg = "Retrying in %.2f seconds ..." % actual_delay
                    if logger is None:
                        logging.exception(msg)
                    else:
                        logger.exception(msg)
                    time.sleep(actual_delay)
                    mtries -= 1
                    mdelay *= 2
            if run_one_last_time:  # one exception may be all the caller wanted in certain cases
                return f(*args, **kwargs)
        return f_retry  # true decorator
    return deco_retry
