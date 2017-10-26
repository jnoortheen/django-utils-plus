import os
from setuptools import find_packages, setup

import utils_plus

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-utils-plus',
    version=utils_plus.__version__,
    packages=find_packages(exclude=['tests*', ]),
    include_package_data=True,
    license='MIT License',
    description='A reusable Django app with small set of utilities for urls, viewsets, commands and more',
    long_description=README,
    url='https://github.com/jnoortheen/django-utils-plus',
    author='Noortheen Raja J',
    author_email='jnoortheen@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
