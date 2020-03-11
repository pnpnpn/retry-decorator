#!/usr/bin/env python

from os.path import exists
from setuptools import setup, find_packages

from retry_decorator import __version__

setup(
        name='retry_decorator',
        version=__version__,
        author='Patrick Ng',
        author_email='pn.appdev@gmail.com',
        scripts=[],
        url='https://github.com/pnpnpn/retry-decorator',
        license='MIT',
        packages=find_packages(),
        description='Retry Decorator',
        long_description=open('README.rst').read() if exists("README.rst") else "",
        install_requires=[],
        classifiers=[
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3 :: Only',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
        ]
)
