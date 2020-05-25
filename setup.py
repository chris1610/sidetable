#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import path
"""
===============================
HtmlTestRunner
===============================


.. image:: https://img.shields.io/pypi/v/sidetable.svg
        :target: https://pypi.python.org/pypi/sidetable
.. image:: https://img.shields.io/travis/chris1610/sidetable.svg
        :target: https://travis-ci.org/chris1610/sidetable

sidetable is a combination of a supercharged pandas `value_counts` plus `crosstab` that 
builds simple but useful summary tables of your pandas DataFrame.


Links:
---------
* `Github <https://github.com/chris1610/sidetable>`_
"""

from setuptools import setup, find_packages
from pathlib import Path
from codecs import open

requirements = ['pandas>=1.0']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    author="Chris Moffitt",
    author_email='chris@moffitts.net',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description="sidetable is like supercharged pandas value_counts that allows you to quickly summarize your data. ",
    install_requires=requirements,
    license="MIT license",
    long_description=long_description,
    include_package_data=True,
    keywords='sidetable',
    name='sidetable',
    packages=find_packages(include=['sidetable']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/chris1610/sidetable',
    version='0.1.0',
    zip_safe=False,
)
