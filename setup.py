from setuptools import setup

from os import path

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
    version='0.0.1',
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
      'console_scripts': ['nbsearch = nbsearch.cli:cli']},
    include_package_data=True,
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
