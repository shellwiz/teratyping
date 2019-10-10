from setuptools import setup, find_packages
from os import environ

with open('requirements.txt') as f:
    requirements = [line.split('--')[0] for line in f.read().splitlines()]

version = environ.get('VERSION', '0.0.1')


setup(name='traftyping',
      author='shellwiz',
      url='https://github.com/shellwiz/traftyping',
      version=version,
      packages=['traftyping', ] + find_packages(),
      license='MIT',
      install_requires=requirements,
      )
