 # coding: utf-8

 import os
 from setuptools import setup, find_packages
 from pip.req import parse_requirements

 CONFIG_PATH = '~/'

 install_reqs = parse_requirements('requirements.txt')
 reqs = [str(ir.req) for ir in install_reqs]

setup(name='sd-bandwidth',
	  version='0.1',
	  description='Command line interface to get bandwidth for a device and interface',
	  author='Jonathan Sundqvist',
	  author_email='jonathan@serverdensity.com',
	  url='',
	  packages=find_packages(),
	  scripts=['sdbandwidth'],
	  install_requires=reqs,
	  data_files=[(os.path.expanduser(CONFIG_PATH), ['sdbandwidth/.config.json'])]
)