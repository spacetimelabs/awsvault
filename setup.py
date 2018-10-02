from setuptools import setup, find_packages
from codecs import open
from os import path

__version__ = '0.0.5'

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='awsvault',
    version=__version__,
    description='AWS secrets manager helper',
    long_description=long_description,
    url='https://github.com/spacetimelabs/awsvault',
    download_url='https://github.com/spacetimelabs/awsvault/tarball/' + __version__,
    license='BSD',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Programming Language :: Python :: 3',
    ],
    keywords='AWS Secrets Manager',
    packages=find_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
    author='Spacetime Labs',
    install_requires=[
        'boto3>=1.9.0,<2.0.0'
    ],
    author_email='dev@spacetimelabs.ai'
)
