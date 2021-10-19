# all_packages

`all_packages` is a Python package that depends on every package on PyPI.

You most certainly will not be able to install this. But if you want to try anyway, execute the following.
```
pip install all_packages
```

To build `all_packages` from source, execute the following. You must use Python 3.8 or higher with the `setuptools` and `wheel` packages present.
```
python configure.py
python setup.py bdist_wheel
```
This creates a wheel file in `dist/`, whose version is based on the current date and time in UTC.
