try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
    name='validate',
    version='0.1',
    author='David W. Fallis',
    author_email='davidwfallis@gmail.com',
    packages=['validate'],
    scripts=[],
    url='',
    description='Model validation package.',
    long_description=open('README.rst').read(),
)

