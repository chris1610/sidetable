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

sidetable builds simple but useful summary tables of your data


Links:
---------
* `Github <https://github.com/chris1610/sidetable>`_
"""

from setuptools import setup, find_packages
from codecs import open

requirements = ['pandas>=1.0']

test_requirements = ['pytest', 'seaborn']

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    author="Chris Moffitt",
    author_email='chris@moffitts.net',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    description="sidetable builds simple but useful summary tables of your data",
    install_requires=requirements,
    license="MIT license",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords='sidetable',
    name='sidetable',
    packages=find_packages(include=['sidetable']),
    python_requires='>=3.6',
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/chris1610/sidetable',
    version='0.8.0',
    zip_safe=False,
)
