# Guide to Uploading Gpgram to PyPI

This guide explains how to upload the Gpgram package to PyPI using API tokens for secure authentication.

## Prerequisites

- A PyPI account (create one at [https://pypi.org/account/register/](https://pypi.org/account/register/))
- Python 3.8 or higher
- The `build` and `twine` packages installed:
  ```bash
  pip install build twine
  ```

## Step 1: Generate a PyPI API Token

1. Log in to your PyPI account at [https://pypi.org/account/login/](https://pypi.org/account/login/)
2. Navigate to your account settings
3. Go to the "API tokens" section
4. Click "Add API token"
5. Enter a token name (e.g., "Gpgram Upload Token")
6. Select the scope:
   - For a project-specific token, select "Scope: Project" and choose "gpgram"
   - For a global token, select "Scope: Entire account"
7. Click "Create token"
8. **IMPORTANT**: Copy the token immediately and store it securely. You won't be able to see it again!

## Step 2: Upload to PyPI Using the API Token

### Option 1: Using the upload_to_pypi.py Script

You can use the provided script to upload the package:

```bash
# Upload to the real PyPI
python upload_to_pypi.py --token "pypi-YOUR_TOKEN_HERE"

# Or upload to TestPyPI first (recommended for testing)
python upload_to_pypi.py --test --token "pypi-YOUR_TOKEN_HERE"
```

### Option 2: Using Environment Variables

You can set the token as an environment variable and run the script:

```bash
# For PyPI
export PYPI_API_TOKEN="pypi-YOUR_TOKEN_HERE"
python upload_to_pypi.py

# For TestPyPI
export TEST_PYPI_API_TOKEN="pypi-YOUR_TOKEN_HERE"
python upload_to_pypi.py --test
```

### Option 3: Manual Upload with Twine

You can also use Twine directly:

```bash
# Build the package
python -m build

# Upload to PyPI
python -m twine upload --username __token__ --password pypi-YOUR_TOKEN_HERE dist/*

# Or upload to TestPyPI
python -m twine upload --repository testpypi --username __token__ --password pypi-YOUR_TOKEN_HERE dist/*
```

## Step 3: Verify the Upload

After uploading, verify that your package is available:

- PyPI: [https://pypi.org/project/gpgram/](https://pypi.org/project/gpgram/)
- TestPyPI: [https://test.pypi.org/project/gpgram/](https://test.pypi.org/project/gpgram/)

## Step 4: Test Installation

Test that your package can be installed:

```bash
# Install from PyPI
pip install gpgram

# Or install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ gpgram
```

## Security Notes

- Never commit your API token to version control
- Use environment variables or secure secret management for CI/CD pipelines
- Rotate your tokens periodically for better security
- Consider using project-scoped tokens instead of account-wide tokens

## Troubleshooting

- **Version conflict**: If you get an error about the version already existing, make sure to update the version number in `setup.py`
- **Invalid classifier**: Check that all classifiers in `setup.py` are valid according to [PyPI's list](https://pypi.org/classifiers/)
- **Invalid long description**: Make sure your README.md is properly formatted
- **Token error**: Ensure you're using the correct token format (`pypi-` prefix included)
