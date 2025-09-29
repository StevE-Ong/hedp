# Updated setup.py with modern practices
#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright CNRS 2012,
# Roman Yurchak (LULI)
# This software is governed by the CeCILL-B license under French law and
# abiding by the rules of distribution of free software.

from setuptools import setup, find_packages, Extension
# Removed duplicate import of find_packages
from Cython.Build import cythonize  # Updated from deprecated Cython.Distutils
import numpy as np

# Optional path to find the GNU scientific library (GSL)
INCLUDE_GSL = None  # "/usr/include"
LIB_GSL = None  # "/usr/lib64"

# Define extensions
ext_modules = [
    Extension("hedp.lib.integrators",
              ["hedp/lib/integrators.pyx"]),
    Extension("hedp.lib.selectors",
              ["hedp/lib/selectors.pyx"]),
]

if INCLUDE_GSL:
    ext_modules.append(Extension("hedp.lib.multigroup",
                                ["hedp/lib/multigroup.pyx"],
                                extra_compile_args=['-O3', '-fopenmp', '-march=native', '-Wall'],
                                extra_link_args=['-O3', '-fopenmp', '-march=native'],
                                libraries=['gsl', 'gslcblas'],
                                library_dirs=[LIB_GSL],
                                ))

setup(
    name='hedp',
    version='0.2.0',  # Updated version
    description='Toolkit for HEDP experiments analysis and postprocessing of related radiative-hydrodynamic simulations',
    author='Roman Yurchak',
    author_email='rth@crans.org',
    packages=find_packages(),
    ext_modules=cythonize(ext_modules),  # Use cythonize instead of deprecated build_ext
    include_dirs=[np.get_include(), INCLUDE_GSL],
    package_data={'hedp': ['hedp/tests/data/*', 'data/db']},
    test_suite="hedp.tests.run",
    python_requires='>=3.8',  # Updated minimum Python version
    install_requires=[
        'numpy>=1.19.0',
        'scipy>=1.5.0',
        'numexpr>=2.7.0',
        'cython>=0.29.0',
        'pytables>=3.6.0',  # Updated package name
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)