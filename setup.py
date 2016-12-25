import sys
from setuptools import setup
from setuptools import find_packages

requirements = ['requests']
if sys.version_info < (2, 7):
    requirements.append('argparse')

setup(name='Reddithor',
      version='0.0.5',
      description='Stay updated with a subreddit of your choice.',
      long_description='Reddithor - a fork of HackerTray - allows you to browse the posts of subreddit of your choice from within the tray of your Linux OS. Reddithor automatically updates every 2 minutes in the background. As mentioned in the readme of HackerTray, this application relies on appindicator, and is not guaranteed to run on every computer. ',
      url='https://github.com/Murtaza0xFF/Reddithor',
      author='Murtaza Akbari',
	  author_email='murtazasakbari@gmail.com',
	  license = 'Apache License, Version 2.0',
	  classifiers=[ 'Development Status :: 4 - Beta'],
	  keywords='reddit Reddithor subreddit Linux',
	  packages=find_packages(),
	  install_requires=[
          'requests>=2.2.1'
      ],
      package_data={
          'Reddithor.data': ['snoo.png']
      },
      entry_points={
          'console_scripts': ['Reddithor = Reddithor:main'],
      })