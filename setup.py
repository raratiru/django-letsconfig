# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='django-letsconfig',
    version='0.1.0',
    description='Base configuration setup for Django',
    long_description=readme,
    author='George Tantiras',
    author_email='',
    url='https://github.com/raratiru/django-letsconfig',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
