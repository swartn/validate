try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup



setup(
    name='validate',
    version='0.1',
    author='David W. Fallis',
    author_email='davidwfallis@gmail.com',
    packages=['validate'],
    package_data={'validate':['configure/*.yaml']},
    scripts=['bin/validate-configure', 'bin/validate-execute'],
    url='',
    description='Model validation package.',
    long_description=open('README.rst').read(),
)

