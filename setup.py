from setuptools import setup
import os
from os import path
from pathlib import Path

def get_requirements(fn='requirements.txt', nogit=True):
   """Get requirements."""
   if path.exists(fn):
      with open(fn, 'r') as f:
        requirements = f.read().splitlines()
   else:
     requirements = []
   requirements = [r.split()[0].strip() for r in requirements if r and not r.startswith('#')]
   if nogit:
       requirements = [r for r in requirements if not r.startswith('git+')]
   return requirements
   
requirements = get_requirements()

print(f'Requirements: {requirements}')

extras = {
    }



setup(
    # Meta
    author='Tony Hirst',
    author_email='tony.hirst@open.ac.uk',
    name='nbsearch',
    url='https://github.com/ouseful-testing/nb-datasette-search',
    version='0.0.2',
    description='datasette powered notebook search',
    long_description='',
    license='MIT License',
    
    # Dependencies
    install_requires=requirements,
    #setup_requires=[],
    extras_require=extras,

    # Packaging
    entry_points={
        'jupyter_serverproxy_servers': [
          'nbsearch = nbsearch:setup_nbsearch',
      ],
      "datasette": ["nbsearch = nbsearch"],
      'console_scripts': ['nbsearch = nbsearch.cli:cli']},
    include_package_data=True,
    package_data={
        "nbsearch": ["static/prism.js",
         "static/clipboard.min.js",
         "static/prism.css",
         "static/marked.min.js",
          "static/nbsearch.css",
         "templates/index.html",
         "static/thebelab.js"
         ],
    },
    zip_safe=False,
    packages=['nbsearch'],

    # Classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Education',
        'License :: Free For Educational Use',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Education'
    ],
)

import subprocess
import sys

def install_external_requirements(fn="external_requirements.txt"):
   """Install additional requiremments eg including installs from github."""
   print(f"Installing external requirements from {fn}")
   try:
      subprocess.check_call([sys.executable, "-m", "pip", "install", "--no-cache-dir", "-r", fn ])
   except:
      print(f"Failed to install {fn}.")
   #requirements = get_requirements(fn, nogit=True)
   #for r in requirements:
   #   print(subprocess.check_output([sys.executable, "-m", "pip", "install", "--no-cache-dir", r ]))
 
install_external_requirements("external_requirements.txt")

"""
from nbsearch.nbsearch import create_init_db
from nbsearch.nbsearch import _NBSEARCH_USER_PATH, _NBSEARCH_DB_PATH
# Create some useful paths
if not os.path.exists(_NBSEARCH_USER_PATH):
    os.makedirs(_NBSEARCH_USER_PATH)
# Would be useful to export these as persistent environment variables?
create_init_db(_NBSEARCH_DB_PATH)
"""