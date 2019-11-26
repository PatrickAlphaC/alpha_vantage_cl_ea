#!/usr/bin/env python

import ast
import re
from setuptools import setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

with open('README.md') as readme_file:
    README = readme_file.read()

setup(
    name='alpha-vantage-cl-ea',
    version=version,
    description='Alpha Vantage official external adapter',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Alpha Vantage',
    author_email='admin@alphavantage.co',
    url='https://github.com/alphavantage/alpha_vantage_cl_ea',
    keywords='financial,timeseries,api,trade,chainlink,blockchain,externaladapter,fintech,stockapi',
    packages=['src'],
    install_requires=[
        'pandas',
        'requests'
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
        'requests-mock',
        'coverage>=4.4.1',
        'mock>=1.0.1',
        'flake8',
    ],
    setup_requires=['pytest-runner', 'flake8'],
)
