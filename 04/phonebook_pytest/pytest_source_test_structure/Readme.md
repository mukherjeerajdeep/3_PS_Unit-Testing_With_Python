# The source code structure and test to be performed 

Settings to run from pycharm

![pyttst](https://user-images.githubusercontent.com/43293317/166119134-e07aec45-f826-4acb-92c7-b11311039d1f.PNG)


`Phonebook Class` 
This project can detect inconsistent lists of phone numbers.

## Usage of this program :  
```text    
    python phonebook < input_data.csv
```

Two thongs to note here, we run the package from the src folder, and the dependency is pytest

```text
    packages=find_packages('src'),
    package_dir={'': 'src'},
    .....
    install_requires=['pytest']    
```

Both the `src` and `test` are packages. We separated out the Test-Fixtures in the `conftest.py` 
script, with the details. Any resources needed for other test to run can be supplied by dependency
injection from this script. 

```python
import pytest

from phonebook.phonenumbers import Phonebook


@pytest.fixture
def phonebook(tmpdir):
    """Provides an empty Phonebook"""
    return Phonebook(tmpdir)
```

Another important file is pytest.ini which serves the configuration of the pytest and influecne the pytest
test runner. 
```text
[pytest]
addopts = --strict
markers =
    slow: Run tests that use sample data from file
```

The `doc` folder contains additional documents for the user, whereas the `sample data` folder tells the location
of the test csv file.  


## Setting up 

However first we need to setup the project by running the `setup.py` so all the requirements and dependancies
must be written there so during setup we instantly get those

```text
python setup.py install
```

Example of the setup.py.

```python
"""Minimal setup file for phonebook project."""

from setuptools import setup, find_packages

setup(
    name='phonebook',
    version='0.1.0',
    description='Manage a collection of phone numbers',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': ['phonebook=phonebook.cli:main'],
    },

    # metadata
    author='Emily Bache',
    author_email='via Pluralsight',
    license='proprietary',
    install_requires=['pytest']
)
```

To run the self tests, use pytest:
```text
    python -m pytest
```

## Tweak the test run by using the pytest annotations.

Here we can see that the test_large_file is rather slow to run than other tests. 
So we can mark that as `@pytest.mark.slow` and the execution can be controlled either by command line or 
the pytest-runner. 

```python
@pytest.mark.slow
def test_large_file(phonebook):
    with open("sample_data/sample1.csv") as f:
        csv_reader = csv.DictReader(f)
```

The command line runner way. with `-m` flag
```text
pytest2>python.exe -m pytest -m "not slow" 
```

However, wrong input in the pytest command-line runner might not guarantee that the tests are executed properly
if the input is wrong, hence the `pytest.ini` comes into picture  

Setting `addopts` to `--strict` option means to only allow the markers to be used. The list of `markers` used 
here is only the `slow`. If we change the marker in the test file with very-slow instead of slow then the 
pytest should warn us that it didn't find very-slow in the list of allowable markers. 

```text
[pytest]
addopts = --strict
markers =
    slow: Run tests that use sample data from file
```

![not_slow](https://user-images.githubusercontent.com/43293317/166119145-6e8ef19f-5efc-400d-b4af-9d9a4e0d0579.PNG)

There are built-in markers in the PyTest, for example the `@pytest.mark.skip("WIP")` which can be used to skip
a test.

```text
pytest2>python.exe -m pytest --markers
@pytest.mark.slow: Run tests that use sample data from file

@pytest.mark.filterwarnings(warning): add a warning filter to the given test. see https://docs.pytest.org/en/stable/how-to/capture-warnings.html#pytest-ma
rk-filterwarnings

@pytest.mark.skip(reason=None): skip the given test function with an optional reason. Example: skip(reason="no way of currently testing this") skips the t
est.

@pytest.mark.skipif(condition, ..., *, reason=...): skip the given test function if any of the conditions evaluate to True. Example: skipif(sys.platform =
= 'win32') skips the test if we are on the win32 platform. See https://docs.pytest.org/en/stable/reference/reference.html#pytest-mark-skipif

```

Another example is the `skipIf` as we can see in the example below. 

```python
@pytest.mark.skipif(sys.version_info < (3, 6),
                    reason="requires python3.6 or higher")
def test_empty_phonebook_is_consistent(phonebook):
    assert phonebook.is_consistent()
```

## Generate html report needs installation of the `pytest-html`

```text
pytest2>python.exe -m pip install pytest-html

Then 
pytest2>python.exe -m pytest --html=report.html
```

