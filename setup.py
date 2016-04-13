try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from validate import __version__


setup(
    name = 'validate',
    version = __version__,
    author = 'David W. Fallis, Neil Swart',
    author_email = 'davidwfallis@gmail.com; neil.swart@canada.ca',
    packages = ['validate'],
    include_package_data = True,
    scripts = ['bin/validate-configure', 'bin/validate-execute'],
    url = 'https://github.com/swartn/validate',
    download_url ='https://github.com/swartn/validate/archive/master.zip',
    description = 'Climate Model validation package',
    long_description = open('README.rst').read(),
    keywords = ['Climate model', 'validation', 'plots', 'CMIP5', 'CMIP6', 'analysis'],
    install_requires = [
        'brewer2mpl >=1.4.1',
        'cdo >=1.2.5',
        'netCDF4 >=1.1.6',
        'matplotlib >=1.4.3',
        'pyyaml >=3.11',
        'basemap >=1.0.7',
        'scipy >=0.15.1',
        'numpy >=1.9.2',
        'cmipdata >=0.6',
    ],
)

#package_data={'validate':['configure/*.yaml']},
