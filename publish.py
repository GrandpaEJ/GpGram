#!/usr/bin/env python
"""
Script to build and publish the package to PyPI.

Usage:
    python publish.py [--test]

Options:
    --test  Publish to TestPyPI instead of PyPI
"""

import os
import sys
import subprocess
import shutil

def run_command(command):
    """Run a shell command and print its output."""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, check=True)
    print(f"Command completed with exit code {result.returncode}")
    return result

def clean_build_dirs():
    """Clean build directories."""
    print("Cleaning build directories...")
    dirs_to_clean = ["build", "dist", "gpgram.egg-info"]
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"Removing {dir_name}...")
            shutil.rmtree(dir_name)

def build_package():
    """Build the package."""
    print("Building package...")
    run_command("python -m build")

def check_package():
    """Check the package with twine."""
    print("Checking package...")
    run_command("python -m twine check dist/*")

def publish_package(test=False):
    """Publish the package to PyPI or TestPyPI."""
    if test:
        print("Publishing to TestPyPI...")
        run_command("python -m twine upload --repository testpypi dist/*")
    else:
        print("Publishing to PyPI...")
        run_command("python -m twine upload dist/*")

def main():
    """Main function."""
    # Check if we should publish to TestPyPI
    test = "--test" in sys.argv

    try:
        # Clean build directories
        clean_build_dirs()

        # Build the package
        build_package()

        # Check the package
        check_package()

        # Publish the package
        publish_package(test=test)

        print("Package published successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error: Command failed with exit code {e.returncode}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
