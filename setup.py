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
    include_package_data=True,
    scripts=['bin/validate-configure', 'bin/validate-execute'],
    url='',
    description='Model validation package.',
    long_description=open('README.rst').read(),
    install_requires=[
        'brewer2mpl ==1.4.1',
        'cdo ==1.2.5',
        'netCDF4 ==1.1.6',
        'numpy ==1.9.2',
        'matplotlib ==1.4.3',
        'pyyaml ==3.11',
    ],
    dependency_links=['https://github.com/swartn/cmipdata.git']
)

