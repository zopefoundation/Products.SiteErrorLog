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

INSTALL_REQUIRES = [
    'setuptools',
    'AccessControl',
    'Acquisition',
    'transaction',
    'zExceptions',
    'Zope >= 4.0b6.dev0',
    'zope.component',
    'zope.interface',
    'zope.event',
]


setup(
    name='Products.SiteErrorLog',
    version='5.0.dev0',
    url='https://github.com/zopefoundation/Products.SiteErrorLog',
    license='ZPL 2.1',
    description="Error log for Zope.",
    author='Zope Foundation and Contributors',
    author_email='zope-dev@zope.org',
    long_description=(open('README.rst').read() + '\n' +
                      open('CHANGES.rst').read()),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Zope Public License",
        "Framework :: Zope :: 4",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    packages=find_packages('src'),
    namespace_packages=['Products'],
    package_dir={'': 'src'},
    install_requires=INSTALL_REQUIRES,
    include_package_data=True,
    zip_safe=False,
)
