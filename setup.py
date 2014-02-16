# -*- coding: utf-8 -*-
import os
import sys
import shutil
import atexit

# Checking for all required packages and if these are recent enough
minimum_numpy_version = "1.6"  # lower versions may work (not tested)
minimum_scipy_version = "0.10" # lower versions may work (not tested)

source_dir = "airballoon"

if not hasattr(sys, 'real_prefix'):
    # Currently only Python 2.7.x is supported
    if sys.version_info[:2] != (2, 7):
        raise RuntimeError("must use python 2.7.x")

    try:
        from setuptools import setup
    except:
        raise RuntimeError("Setuptools not found, setup cannot continue without it")

    try:
        import numpy as np
    except:
        raise RuntimeError("Numpy not found")
    if np.__version__ < minimum_numpy_version:
        print("*Error*: NumPy version is lower than needed: %s < %s" %
              (np.__version__, minimum_numpy_version))
        sys.exit(1)

    try:
        import scipy
    except:
        raise RuntimeError("Scipy not found")
    if scipy.__version__ < minimum_scipy_version:
        print("*Error*: Scipy version is lower than needed: %s < %s" %
              (scipy.__version__, minimum_scipy_version))
        sys.exit(1)

else:
    from setuptools import setup

# Walk through the subdirs and add all non-python scripts to MANIFEST.in
def create_manifest():
    print 'creating manifest.in'
    matches = []
    for root, dirnames, filenames in os.walk(source_dir):
        if ('.git' in str(root)) == False:
            for filename in filenames:
                if filename.endswith(('.py', '.pyc')) == False:
                  matches.append(os.path.join(root, filename))
    for root, dirnames, filenames in os.walk('docs'):
        if ('.git' in str(root)) == False:
            for filename in filenames:
                if filename.endswith(('.py', '.pyc')) == False:
                  matches.append(os.path.join(root, filename))
    # Manually add extra files from the top-level directory
    matches.append(os.path.join(os.path.dirname(__file__),'INSTALL.txt'))
    matches.append(os.path.join(os.path.dirname(__file__),'LICENSE.txt'))

    with open('MANIFEST.in', 'w') as f:
        f.writelines(("include %s\n" % l.replace(' ','?') for l in matches))

# To remove the manifest file after installation
def delete_manifest():
    if os.path.exists('MANIFEST.in'):
        os.remove('MANIFEST.in')

# Create list for Python scripts directories to include
def get_packages():
    print 'searching for packages'
    matches = []
    for root, dirnames, filenames in os.walk(source_dir):
        if ('.git' in str(root)) == False:
            for filename in filenames:
                if filename.endswith(('.py', '.pyc')) == True and not filename.startswith('setup'):
                    matches.append(root)
    matches = list(set(matches))
    return matches

def del_dir(dirname):
    if os.path.exists(dirname):
        shutil.rmtree(dirname)

def setup_package():
    create_manifest()
    list = ['Numpy>=1.6','Scipy>=0.1']
    setup(
        name = "airballoon",
        version = "1.0",
        author = "Brett M. Morris",
        author_email = "bmmorris@uw.edu",
        description = ("Calculate astronomical airmass for sub-orbital"+\
                       "observatories at high elevations."),
        license = 'LICENSE.txt',
        keywords = "astronomy airmass high elevation",
        url = "https://github.com/bmorris3/airballoon",
        packages=get_packages(),
        include_package_data = True,
        zip_safe = False,
        long_description=open(os.path.join(os.path.dirname(\
                      os.path.abspath(__file__)),'README.md')).read(),
        download_url='https://github.com/bmorris3/airballoon/archive/master.zip',
         install_requires=list,
        classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.7',
          'Topic :: Scientific/Engineering :: Astronomy',
          'Topic :: Scientific/Engineering :: Physics'
      ],
    )

# At exit delete temporary files
def to_do_at_exit():
    delete_manifest()
    del_dir('build')

    if 'install' in sys.argv:
        del_dir('dist')

#Set function to be executed at exit of code (when script is finished)
atexit.register(to_do_at_exit)

if __name__ == '__main__':
    setup_package()