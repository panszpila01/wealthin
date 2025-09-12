# Troubleshooting Guide

## Common Issues and Solutions

### 1. NumPy/PyArrow Compatibility Error

**Error Message:**
```
A module that was compiled using NumPy 1.x cannot be run in NumPy 2.2.4 as it may crash.
AttributeError: _ARRAY_API not found
ImportError: numpy.core.multiarray failed to import
```

**Solution:**
This error occurs due to version incompatibility between NumPy 2.x and PyArrow. To fix:

1. **Update requirements.txt** (already done):
   ```
   numpy<2.0.0
   pyarrow>=10.0.0
   ```

2. **Reinstall packages:**
   ```bash
   # Activate virtual environment
   source venv/bin/activate
   
   # Uninstall problematic packages
   pip uninstall numpy pyarrow -y
   
   # Reinstall with correct versions
   pip install "numpy<2.0.0" "pyarrow>=10.0.0"
   ```

3. **Alternative solution** (if above doesn't work):
   ```bash
   pip install --force-reinstall --no-deps "numpy<2.0.0"
   pip install --force-reinstall --no-deps "pyarrow>=10.0.0"
   ```

### 2. Import Errors

**Error:** `ModuleNotFoundError: No module named 'src'`

**Solution:**
Make sure you're running the application from the project root directory:
```bash
cd /path/to/Koteria
streamlit run main.py
```

### 3. Virtual Environment Issues

**Error:** `command not found: pip` or `command not found: streamlit`

**Solution:**
Activate your virtual environment:
```bash
# On macOS/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

### 4. Port Already in Use

**Error:** `Port 8501 is already in use`

**Solution:**
Either:
- Stop the existing Streamlit process
- Or run on a different port:
  ```bash
  streamlit run main.py --server.port 8502
  ```

### 5. File Upload Issues

**Error:** File upload not working or unsupported file type

**Solution:**
1. Check that your file is in a supported format (CSV, Excel)
2. Ensure the file is not corrupted
3. Try with a smaller file first
4. Check browser console for JavaScript errors

### 6. Authentication Issues

**Error:** Login not working

**Solution:**
1. Check credentials in the configuration
2. Clear browser cache and cookies
3. Try incognito/private browsing mode
4. Check that session state is properly initialized

## Environment Setup

### Fresh Installation

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run application:**
   ```bash
   streamlit run main.py
   ```

### Development Setup

For development, you might want to install additional packages:
```bash
pip install black flake8 pytest
```

## Getting Help

If you encounter issues not covered here:

1. Check the [Streamlit documentation](https://docs.streamlit.io/)
2. Search for similar issues on [GitHub Issues](https://github.com/streamlit/streamlit/issues)
3. Check the [NumPy compatibility guide](https://numpy.org/devdocs/numpy_2_0_migration_guide.html)
4. Create an issue in this repository with:
   - Error message
   - Python version
   - Package versions (`pip list`)
   - Steps to reproduce
