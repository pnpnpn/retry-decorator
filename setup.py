# -*- coding: utf-8 -*-
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup( 
        name='retry_decorator',
        version='0.1.0',
        description='Retry Decorator',
        long_description = 'See homepage for usage',
        author='Patrick Ng',
        author_email='pn.appdev@gmail.com',
        url='https://github.com/pnpnpn/retry-decorator',
        packages=['retry_decorator'],
        )

