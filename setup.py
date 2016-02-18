try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from validate import __version__


setup(
    name = 'validate',
    version = __version__,
    author = 'David W. Fallis',
    author_email = 'davidwfallis@gmail.com',
    packages = ['validate'],
    include_package_data = True,
    scripts = ['bin/validate-configure', 'bin/validate-execute'],
    url = '',
    description = 'Model validation package.',
    long_description = open('README.rst').read(),
    install_requires = [
        'brewer2mpl >=1.4.1',
        'cdo >=1.2.5',
        'netCDF4 >=1.1.6',
        'numpy >=1.9.2',
        'matplotlib >=1.4.3',
        'pyyaml >=3.11',
        'basemap >=1.0.7',
        'scipy >=0.15.0',
    ],
)

#package_data={'validate':['configure/*.yaml']},
