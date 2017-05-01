#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Pyrrigate',
    version='0.0.1',
    description='A simple system to manage automated irrigation for home gardens.',
    long_description=readme,
    author='H. Stefan Puhlmann',
    author_email='hugopuhlmann@gmail.com',
    url='https://github.com/hstefan/pyrrigate',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

