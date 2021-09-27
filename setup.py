from setuptools import setup
from setuptools import find_packages

setup(
    name='cereal',
    version='1.0',
    author='Jason Walsh',
    author_email='rightlag@gmail.com',
    url='https://github.com/cereal-io/cereal-py',
    description='''
        Convert Google Protocol Buffers, Apache Avro, and Apache Thrift
        files to their respective counterparts.
    ''',
    license='MIT',
    packages=find_packages(),
    package_data={'cereal': ['patterns.json']},
    include_package_data=True,
)
