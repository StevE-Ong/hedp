#!/usr/bin/env python3
"""
Automated script to update deprecated functions in the HEDP repository.

This script applies all the necessary fixes to modernize the codebase:
1. Replace numpy.fromstring with numpy.frombuffer
2. Update Cython setup to use modern practices
3. Remove deprecated __future__ imports
4. Fix duplicate imports
5. Update Python version requirements

Usage:
    python fix_deprecated_functions.py /path/to/hedp/repository
"""

import os
import re
import sys
from pathlib import Path


def fix_numpy_fromstring(file_path):
    """Replace deprecated np.fromstring with np.frombuffer for binary data."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace numpy.fromstring without sep parameter with frombuffer
    # This pattern matches cases where no sep is specified or sep=''
    pattern = r'np\.fromstring\s*\(\s*([^,)]+)\s*,\s*(dtype\s*=\s*[^,)]+)(?:\s*,\s*count\s*=\s*[^,)]+)?\s*\)'
    
    def replacement(match):
        buffer_arg = match.group(1)
        dtype_arg = match.group(2)
        return f'np.frombuffer({buffer_arg}, {dtype_arg})'
    
    updated_content = re.sub(pattern, replacement, content)
    
    if content != updated_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"âœ… Fixed numpy.fromstring in {file_path}")
        return True
    return False


def fix_future_imports(file_path):
    """Remove deprecated __future__ imports."""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    updated_lines = []
    removed_imports = []
    
    future_imports = [
        'absolute_import',
        'division', 
        'print_function',
        'unicode_literals'
    ]
    
    for line in lines:
        # Check if line contains a __future__ import
        is_future_import = False
        for import_name in future_imports:
            if re.match(rf'from\s+__future__\s+import\s+.*{import_name}', line.strip()):
                is_future_import = True
                removed_imports.append(import_name)
                break
        
        if not is_future_import:
            updated_lines.append(line)
        else:
            # Replace with a comment
            updated_lines.append(f"# REMOVED: {line.strip()}\n")
    
    if removed_imports:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(updated_lines)
        print(f"âœ… Removed __future__ imports {removed_imports} from {file_path}")
        return True
    return False


def fix_setup_py(file_path):
    """Update setup.py to use modern Cython practices."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Replace Cython.Distutils import
    content = re.sub(
        r'from Cython\.Distutils import build_ext',
        'from Cython.Build import cythonize',
        content
    )
    
    # Remove duplicate find_packages import
    lines = content.split('\n')
    seen_find_packages = False
    updated_lines = []
    
    for line in lines:
        if 'from setuptools import' in line and 'find_packages' in line:
            if seen_find_packages:
                updated_lines.append('# REMOVED: Duplicate import')
                continue
            seen_find_packages = True
        updated_lines.append(line)
    
    content = '\n'.join(updated_lines)
    
    # Update setup() call to use cythonize
    content = re.sub(
        r'cmdclass\s*=\s*{[^}]*build_ext[^}]*}',
        'ext_modules=cythonize(ext_modules)',
        content
    )
    
    # Add modern Python requirements
    if 'python_requires' not in content:
        # Find the setup( call and add python_requires
        setup_pattern = r'(setup\s*\([^)]*)'
        replacement = r'\1\n    python_requires=">=3.8",'
        content = re.sub(setup_pattern, replacement, content, flags=re.DOTALL)
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"âœ… Updated setup.py with modern practices")
        return True
    return False


def update_requirements_txt(file_path):
    """Update requirements.txt with version pins."""
    if not os.path.exists(file_path):
        print(f"âš ï¸  {file_path} not found, skipping")
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Map old package names to new ones with versions
    package_mapping = {
        'numpy': 'numpy>=1.19.0',
        'scipy': 'scipy>=1.5.0', 
        'numexpr': 'numexpr>=2.7.0',
        'cython': 'cython>=0.29.0',
        'tables': 'pytables>=3.6.0'
    }
    
    updated_lines = []
    for line in lines:
        package = line.strip()
        if package in package_mapping:
            updated_lines.append(package_mapping[package] + '\n')
        else:
            updated_lines.append(line)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(updated_lines)
    
    print(f"âœ… Updated {file_path} with version constraints")
    return True


def scan_repository(repo_path):
    """Scan repository for files that need updates."""
    repo_path = Path(repo_path)
    
    if not repo_path.exists():
        print(f"âŒ Repository path {repo_path} does not exist")
        return False
    
    print(f"ðŸ” Scanning repository: {repo_path}")
    
    changes_made = False
    
    # Find and fix Python files
    python_files = list(repo_path.rglob("*.py"))
    
    for py_file in python_files:
        print(f"\nðŸ“ Checking {py_file.relative_to(repo_path)}")
        
        # Fix numpy.fromstring issues
        if fix_numpy_fromstring(py_file):
            changes_made = True
        
        # Fix __future__ imports
        if fix_future_imports(py_file):
            changes_made = True
        
        # Special handling for setup.py
        if py_file.name == 'setup.py':
            if fix_setup_py(py_file):
                changes_made = True
    
    # Update requirements.txt
    req_file = repo_path / 'requirements.txt'
    if update_requirements_txt(req_file):
        changes_made = True
    
    return changes_made


def main():
    """Main function."""
    if len(sys.argv) != 2:
        print("Usage: python fix_deprecated_functions.py /path/to/hedp/repository")
        sys.exit(1)
    
    repo_path = sys.argv[1]
    
    print("ðŸš€ HEDP Repository Modernization Script")
    print("="*50)
    
    changes_made = scan_repository(repo_path)
    
    print("\n" + "="*50)
    if changes_made:
        print("âœ… Modernization complete! Changes were made to the repository.")
        print("\nðŸ“‹ Next steps:")
        print("1. Test the updated code with Python 3.8+")
        print("2. Run the test suite to ensure functionality")
        print("3. Update documentation to reflect Python 3.8+ requirement")
        print("4. Consider bumping version to 0.2.0")
    else:
        print("â„¹ï¸  No deprecated functions found or all already updated.")
    
    print("\nðŸ”§ Manual review recommended for:")
    print("- Any custom Cython extensions")
    print("- Platform-specific code")
    print("- Documentation updates")


if __name__ == "__main__":
    main()