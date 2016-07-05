# -*- coding: utf-8 -

import os
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

# read dev requirements
fname = os.path.join(os.path.dirname(__file__), 'requirements.txt')
with open(fname) as f:
    tests_require = [l.strip() for l in f.readlines()]

if sys.version_info[:2] < (2, 7):
    tests_require.append('unittest2')


class PyTestCommand(TestCommand):
    user_options = [
        ("cov", None, "measure coverage")
    ]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.cov = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['tests']
        if self.cov:
            self.test_args += ['--cov']
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

setup(
    name='rabbit2ev',
    description='Bind RabbitMq messages with custom plugin',
    author='Ezequiel Lovelle',
    author_email='ezequiellovelle@gmail.com',
    license='MIT',
    zip_safe=False,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    tests_require=tests_require,
    cmdclass={'test': PyTestCommand},
)
