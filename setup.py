from setuptools import setup
import os
import sys
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass into py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        try:
            from multiprocessing import cpu_count
            self.pytest_args = ['-n', str(cpu_count()), '--boxed']
        except (ImportError, NotImplementedError):
            self.pytest_args = ['-n', '1', '--boxed']

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


with open(os.path.join(os.path.dirname(__file__), 'description.md')) as file:
    long_description = file.read()

with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as reqs:
    install_requires = [line for line in reqs.read().split('\n') if (line and not line.startswith('--'))]

with open(os.path.join(os.path.dirname(__file__), 'requirements_test.txt')) as reqs:
    test_requirements = [line for line in reqs.read().split('\n') if (line and not line.startswith('--'))]

setup(
    name='sos_api_client',
    author="sos data team",
    version='1.0',
    packages=['api_client'],
    zip_safe=False,
    python_requires='>=3.7',
    description='sos api client',
    license="GPLv3+",
    long_description=long_description,
    install_requires=install_requires,
    cmdclass={'test': PyTest},
    tests_require=test_requirements,
    classifiers=[
        'Development Status :: Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Framework :: Flask',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
