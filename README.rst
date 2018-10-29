.. image:: https://badge.fury.io/py/retry_decorator.svg
    :target: https://badge.fury.io/py/retry_decorator

.. image:: https://travis-ci.org/pnpnpn/retry-decorator.svg?branch=master
    :target: https://travis-ci.org/pnpnpn/retry-decorator

Usage
-----

Retry decorator

::

    #!/usr/bin/env python

    from __future__ import print_function
    from retry_decorator import *

    @retry(RuntimeError, KeyError, tries = 3, timeout_secs = 0.1)
    def test_retry():
        import sys
        print('hello', file = sys.stderr)
        raise RuntimeError('Testing retry')

    if __name__ == '__main__':
        try:
            test_retry()
        except Exception as e:
            print('Received the last exception')


Contribute
----------
I would love for you to fork and send me pull request for this project. Please contribute.
