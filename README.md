#   HEDP module

[![Build Status](https://travis-ci.org/luli/hedp.svg?branch=master)](https://travis-ci.org/luli/hedp)

A Python module to analyse High Energy Density (HED) experiments and radiation hydrodynamics simulations.


## Installation

    python setup.py develop --user


## Dependencies
   This module requires Python 2.7, 3.3 or 3.4  with  `numpy`, `scipy`,  `cython`, `pytables` and `opacplot2` ( https://github.com/rth/opacplot2).


 Optional dependencies include:
 - `matplotlib`
 - `beautifulsoup4`
 - The GNU Scientific Library (GSL), required for calculating the Planck/Rosseland means
 - PyEOSPAC (https://github.com/luli/pyeospac), for interfacing with the tabulated EoS
 - `nose`, for running the test suite

## List of features
  
####   File formats `hedp.io`

   - parser for the Andor `.sif` image files
   - parser for the Hamamatsu streak camera `.img` files

#### Equation of state (EoS) and opacities
   - Kramer-Unsoldt opacity model
   - generation of a database with cold henke opacities
   - Thomas Fermi pressure ionization.
   - Calculation of Planck and Rosseland (gray/mutigroup) means
   - Automatic group selection for multigroup opacities
   - General interpolators intended for visualisation for the EoS and opacity tables (requires [opacplot](https://github.com/rth/opacplot2) and [pyeospac](https://github.com/luli/pyeospac) modules).


####  Basic mathematical operators `hedp.math`
   - Gradient for a non-informally sampled 1D or 2D data
   - Savitzky-Golay filter 
   - Integrators for the super-gaussian functions
   - Direct and inverse Abel transforms. The integration is carried out numerically with a semi-analytical handling of the singularity.


#### Plasma physics `hedp.plasma_physics`
   Defines a few useful quantities  in plasma physics:  the critical density, Coulomb logarithm, electron-ion collision rates, inverse Bremsstrahlung coefficient,  isentropic sound speed, Spitzer conductivity.


#### Visualization  `hedp.viz`
   - Metric formatter for `matplotlib`
         
#### Diagnostics  `hedp.diag`
   - intensity calibration for the self-emission GOI and SOP
   - IP sensitivity curves for x-rays
   

#### Post-processing  `hedp.pp`
   - Calculation of synthetic radiographs from 2D axis-symmetrical hydrodynamic simulation with the Abel transform 

# HEDP Repository Migration Guide: Removing Deprecated Functions

This guide provides step-by-step instructions for updating the HEDP repository to remove deprecated Python functions and modernize the codebase.

## Overview

The HEDP (High Energy Density Physics) repository contains several deprecated functions that need to be updated for compatibility with modern Python versions and libraries. This repository was last updated 9-12 years ago and requires significant modernization.

## Summary of Changes Required

### 1. Python Version Requirements
- **Current**: Supports Python 2.7, 3.3, 3.4
- **Updated**: Require Python 3.8+ minimum
- **Reason**: Python 2.7 was deprecated on January 1, 2020. Python 3.3-3.7 are now end-of-life.

### 2. Deprecated Functions to Fix

#### A. `numpy.fromstring()` â†’ `numpy.frombuffer()`
**File**: `hedp/io/andor.py`
**Line**: ~77

**Before**:
```python
self.data = np.fromstring(raw_data, dtype=np.float32)
```

**After**:
```python
self.data = np.frombuffer(raw_data, dtype=np.float32)
```

**Reason**: The binary mode of `fromstring()` is deprecated since NumPy 1.14. `frombuffer()` is the recommended replacement for binary data.

#### B. `Cython.Distutils.build_ext` â†’ `Cython.Build.cythonize`
**File**: `setup.py`
**Lines**: 8-9, 36

**Before**:
```python
from Cython.Distutils import build_ext
# ... 
cmdclass = {'build_ext': build_ext},
```

**After**:
```python
from Cython.Build import cythonize
# ...
ext_modules = cythonize(ext_modules),
```

**Reason**: `Cython.Distutils.build_ext` is deprecated since Cython 0.25. The modern approach uses `cythonize()`.

#### C. Remove `__future__` imports
**File**: `hedp/math/abel.py`
**Lines**: 8-11

**Before**:
```python
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
```

**After**:
```python
# These imports removed - no longer needed for Python 3.8+
```

**Reason**: These imports were for Python 2/3 compatibility and are deprecated in Python 3.14+.

#### D. Fix duplicate imports
**File**: `setup.py`
**Lines**: 7-8

**Before**:
```python
from setuptools import setup, find_packages, Extension
from setuptools import find_packages  # duplicate!
```

**After**:
```python
from setuptools import setup, find_packages, Extension
```

### 3. Dependency Updates

#### A. Update `requirements.txt`
**Before**:
```
numpy
scipy
numexpr
cython
tables
```

**After**:
```
numpy>=1.19.0
scipy>=1.5.0
numexpr>=2.7.0
cython>=0.29.0
pytables>=3.6.0
```

#### B. Update setup.py dependencies
Add to `setup.py`:
```python
python_requires='>=3.8',
install_requires=[
    'numpy>=1.19.0',
    'scipy>=1.5.0',
    'numexpr>=2.7.0',
    'cython>=0.29.0',
    'pytables>=3.6.0',
],
```

## Implementation Steps

### Step 1: Update Python Version Requirements
1. Edit `setup.py` to require Python 3.8+
2. Update any documentation mentioning Python 2.7 support
3. Test with Python 3.8, 3.9, 3.10, 3.11, 3.12

### Step 2: Fix NumPy Deprecation
1. Locate all uses of `np.fromstring()` without `sep` parameter
2. Replace with `np.frombuffer()` for binary data
3. Ensure data types remain consistent

### Step 3: Modernize Cython Setup
1. Replace `Cython.Distutils.build_ext` with `Cython.Build.cythonize`
2. Update `setup.py` to use modern setuptools practices
3. Test Cython extension compilation

### Step 4: Remove Future Imports
1. Remove all `from __future__ import` statements
2. Verify code still works without them (should be fine for Python 3.8+)
3. Check for any Python 2 specific syntax that needs updating

### Step 5: Update Dependencies
1. Pin minimum versions for all dependencies
2. Update package names (e.g., `tables` â†’ `pytables`)
3. Test installation and functionality

## Testing Strategy

1. **Unit Tests**: Run existing test suite with updated code
2. **Python Versions**: Test with Python 3.8, 3.9, 3.10, 3.11, 3.12
3. **Dependencies**: Test with minimum and latest versions of dependencies
4. **Integration**: Ensure scientific functionality remains intact

## Compatibility Notes

### Breaking Changes
- Drops support for Python < 3.8
- May require users to update their Python environment
- Some very old NumPy versions no longer supported

### Non-Breaking Changes
- All scientific functionality preserved
- API remains the same
- Performance should improve with modern Python

## Migration Commands

After making the code changes, users should:

```bash
# Remove old installation
pip uninstall hedp

# Install updated version
pip install -e .

# Or for development
python setup.py develop --user
```

## Additional Recommendations

1. **Add CI/CD**: Set up GitHub Actions for automated testing
2. **Type Hints**: Consider adding type hints for better code quality
3. **Documentation**: Update documentation to reflect Python 3.8+ requirement
4. **Version Bump**: Update version to 0.2.0 to indicate breaking changes

## Files Modified

- `setup.py` - Major modernization
- `hedp/io/andor.py` - NumPy deprecation fix
- `hedp/math/abel.py` - Remove future imports
- `requirements.txt` - Version pinning
- Any other files with `from __future__ import` statements

## Verification

After implementing these changes:
1. Code should install cleanly on Python 3.8+
2. No deprecation warnings should appear
3. All existing functionality should work
4. Tests should pass
5. Scientific computations should produce identical results

This migration brings the HEDP repository up to modern Python standards while preserving all scientific functionality.