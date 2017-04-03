#!/usr/bin/env python

from setuptools import setup

setup(
    name='pytest-nice',
    description='pytest plugin to make even nicer html reports',
    version="v0.1",
    author='Jonas Zinn',
    author_email='Jonas.S.Zinn@gmail.com',
    url='https://github.com/zinnjonas/pytest-nice',
    packages=['pytest_nice'],
    entry_points = {
        'pytest11': [
            'nice = pytest_nice',
        ]
    },
    install_requires=['pytest', 'pytest-html', 'pytest-pep8', 'pytest-flakes', 'pytest-cov'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
