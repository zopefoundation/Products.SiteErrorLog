# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2010 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

from setuptools import setup, find_packages

setup(
    name='Products.SiteErrorLog',
    version='3.0.dev0',
    url='http://pypi.python.org/pypi/Products.SiteErrorLog',
    license='ZPL 2.1',
    description="error log for Zope 2.",
    author='Zope Foundation and Contributors',
    author_email='zope-dev@zope.org',
    long_description=(open('README.rst').read() + '\n' +
                      open('CHANGES.txt').read()),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Zope Public License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2 :: Only",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Framework :: Zope2",
    ],
    packages=find_packages('src'),
    namespace_packages=['Products'],
    package_dir={'': 'src'},
    extras_require=dict(
        test=['transaction'],
    ),
    install_requires=[
        'setuptools',
        'AccessControl',
        'Acquisition',
        'zExceptions',
        'Zope2',
        'zope.component',
        'zope.interface',
        'zope.event',
    ],
    include_package_data=True,
    zip_safe=False,
)
