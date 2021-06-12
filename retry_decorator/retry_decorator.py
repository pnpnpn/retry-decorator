#
# License: MIT
# Copyright: Patrick Ng - 2012
#

import logging
import time
import random
import types


def _isiter(i):
    if not isinstance(i, (list, tuple)):
        return False
    elif len(i) != 2:
        raise ValueError("provided list|tuple needs to have size of 2")
    return True


def _deco_retry(f, exc=Exception, tries=10, timeout_secs=1.0, logger=None, callback_by_exception=None):
    """
    Common function logic for the internal retry flows.
    :param f:
    :param exc:
    :param tries:
    :param timeout_secs:
    :param logger:
    :param callback_by_exception:
    :return:
    """
    def f_retry(*args, **kwargs):
        mtries, mdelay = tries, timeout_secs
        run_one_last_time = True
        while mtries > 1:
            try:
                return f(*args, **kwargs)
            except exc as e:
                # check if this exception is something the caller wants special handling for
                if isinstance(callback_by_exception, (types.FunctionType, list, tuple)):
                    callback_by_exception = {Exception: callback_by_exception}
                callback_errors = callback_by_exception or {}

                for error_type in callback_errors:
                    if isinstance(e, error_type):
                        callback_logic = callback_by_exception[error_type]
                        should_break_out = run_one_last_time = False  # TODO: why is run_one_last_time default value changed when callback_by_exception is defined?
                        if _isiter(callback_logic):
                            callback_logic, should_break_out = callback_logic
                            if _isiter(should_break_out):
                                should_break_out, run_one_last_time = should_break_out
                        callback_logic()
                        if should_break_out:  # caller requests we stop handling this exception
                            break
                half_interval = mdelay * 0.10  # interval size
                actual_delay = random.uniform(mdelay - half_interval, mdelay + half_interval)
                msg = "Retrying in %.2f seconds ..." % actual_delay
                logging_object = logger or logging
                logging_object.exception(msg)
                time.sleep(actual_delay)
                mtries -= 1
                mdelay *= 2
        if run_one_last_time:  # one exception may be all the caller wanted in certain cases
            return f(*args, **kwargs)

    return f_retry  # true decorator


def retry(exc=Exception, tries=10, timeout_secs=1.0, logger=None, callback_by_exception=None):
    """
    Retry calling the decorated function using an exponential backoff.

    :param exc: catch all exceptions, a specific exception, or an iterable of exceptions
    :param tries: how many attempts to retry when catching those exceptions
    :param timeout_secs: general delay between retries (we do employ a jitter)
    :param logger: an optional logger object
    :param callback_by_exception: callback/method invocation on certain exceptions
    :type callback_by_exception: None, list, tuple, function or dict
    """
    # We re-use `RetryHandler` so that we can reduce duplication; decorator is still useful!
    retry_handler = RetryHandler(exc, tries, timeout_secs, logger, callback_by_exception)
    return retry_handler


class RetryHandler(object):
    """
    Class supporting a more programmatic approach (not requiring a decorator) for retrying logic.
    """
    __slots__ = ["exc", "tries", "timeout_secs", "logger", "callback_by_exception"]

    def __init__(
            self, exc=Exception, tries=10, timeout_secs=1.0, logger=None, callback_by_exception=None,
    ):
        if not isinstance(tries, int):
            raise TypeError("[tries] arg needs to be of int type")
        elif tries < 1:
            raise ValueError("[tries] arg needs to be an int >= 1")

        self.exc = exc
        self.tries = tries
        self.timeout_secs = timeout_secs
        self.logger = logger
        self.callback_by_exception = callback_by_exception
        super().__init__()

    def __call__(self, f, *args, **kwargs):
        retry_return = _deco_retry(
            f, self.exc, self.tries, self.timeout_secs, self.logger, self.callback_by_exception,
        )
        return retry_return
