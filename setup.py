#!/usr/bin/python3 -tt
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name = 'usazovator',
    version = '1',
    author = 'NTK',
    description = ('physical security management'),
    license = 'MIT',
    keywords = 'physical security management',
    url = 'http://github.com/techlib/usazovator',
    packages=[
        'usazovator',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
    ],
    scripts=['bin/usazovator']
)


# vim:set sw=4 ts=4 et:
