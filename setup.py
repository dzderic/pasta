#!/usr/bin/env python
from setuptools import setup

setup(
    name = 'Pasta',
    version = '0.0.1',
    #description = 'Python Distribution Utilities',
    #url = 'http://www.python.org/sigs/distutils-sig/',
    packages = open('requirements.txt').read().split(),
)
