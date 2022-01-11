# all_packages

The Python Package Index (PyPI) contains over 300,000 Python packages. Need a
Python library but don't want to search through all the options? Search no
further! `all_packages` is a Python script that attempts to install every
package on PyPI - all {:,} of them as of {}.

## Install
```
pip install all_packages
```

## Run
From the command line, execute the following.
```
all_packages install
```
For each package on PyPI, this creates a virtual environment in the
`all_packages` subdirectory of your home directory and attempts to install the
package into that virtual environment.

To customize where the virtual environments are created, use the `-d` option.
```
all_packages install -d MYDIRECTORY
```
