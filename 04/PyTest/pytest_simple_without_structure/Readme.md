# Pytest is another way to test the python source code, it's more pythonic than the unittest

It can be executed from the command line as well. With option `-v` means verbose to show
the progress.

```text
pytest1>python.exe -m pytest -v
================================================================== test session starts ================================================================== 
platform win32 -- Python 3.10.2, pytest-7.1.2, pluggy-1.0.0 -- C:\Python\python.exe
cachedir: .pytest_cache
rootdir: C:\Rajdeep_Mukherjee\PluralSight_Python\3_PS_Unit-Testing_With_Python\04\phonebook_pytest\pytest1
collected 3 items                                                                                                                                         

test_phonebook.py::test_lookup_by_name PASSED                                                                                                      [ 33%] 
test_phonebook.py::test_phonebook_contains_all_names PASSED                                                                                        [ 66%] 
test_phonebook.py::test_missing_name_raises_error PASSED                                                                                           [100%] 

=================================================================== 3 passed in 0.03s =================================================================== 
```

## Now for the test case as below, we can fail the test case.

```python
def test_phonebook_contains_all_names(phonebook):
    phonebook.add("Bob", "1234")
    assert "Bob" in phonebook.names()
    assert "Missing" in phonebook.names() # This will fail the test
```
Because here `Bob` is present in the phonebook but the `Missing` is not, however we checked with assertion
that `Missing` is in phonebook or not. So that the TC fails with error 

```yaml
Expected :{'Bob'}
Actual   :'Missing'
```

```python
Expected :{'Bob'}
Actual   :'Missing'
<Click to see difference>

phonebook = <phonebook.Phonebook object at 0x0000016757C0DED0>

    def test_phonebook_contains_all_names(phonebook):
        phonebook.add("Bob", "1234")
        assert "Bob" in phonebook.names()
>       assert "Missing" in phonebook.names() # This will fail the test
E       AssertionError: assert 'Missing' in {'Bob'}
E        +  where {'Bob'} = <bound method Phonebook.names of <phonebook.Phonebook object at 0x0000016757C0DED0>>()
E        +    where <bound method Phonebook.names of <phonebook.Phonebook object at 0x0000016757C0DED0>> = <phonebook.Phonebook object at 0x0000016757C0DED0>.names

test_phonebook.py:20: AssertionError
```

## Raise an Error if the phonebook is non-empty

Same happened for the case when we want to check if the phone book is empty or not, if it is empty 
then raise an error. This TC fails as we included `Bob` into the phonebook and the ValueError was never
raised. 

```python
def test_missing_name_raises_error(phonebook):
    phonebook.add("Bob", "1234")  # This will fail the test, because Bob is actually present
    with pytest.raises(KeyError):
        phonebook.lookup("Bob")
```

### **This is the way pytest asserts the Exception.** 

Due to presence of Bob in the list the TC fails. 

```python
test_phonebook.py::test_missing_name_raises_error FAILED                 [100%]
test_phonebook.py:23 (test_missing_name_raises_error)
phonebook = <phonebook.Phonebook object at 0x0000016757BFFCA0>

    def test_missing_name_raises_error(phonebook):
        phonebook.add("Bob", "1234")  # This will fail the test, because Bob is actually present
>       with pytest.raises(KeyError):
E       Failed: DID NOT RAISE <class 'KeyError'>

test_phonebook.py:26: Failed
```

## How `PyTest` handles the `Test-Fixtures`

`Test-Fixtures` are the systematic flow of the test in python, in unittest we used them by overriding the 
`setup()` and `teardown()` methods from the `unittest.Testcase` class. 

In unittest it's used as this. 

```python
class PhoneBookTest(unittest.TestCase):

    # Setup and Teardown will run for each test cases
    def setUp(self) -> None:
        self.phonebook = PhoneBook()

    # Maybe needed when the resources are needed to be cleaned up,
    # here it is not needed.
    def tearDown(self) -> None:
        pass
```

**Then how Pytest handles those ?**

When a test is going to be executed in PyTest, it looks for the decorator named `@pytest.fixture` and get
the resources from there. It's a kind of runtime, because it's only needed when the tests are executed. 

We can say it similar like **DI(Dependency Injection)** for that specific tests during runtime.  
In this case we returned the PhoneBook object as our tests depends on that. We can replace that with Mock
as well, and that's the beauty of using this DI. 

In this case `phonebook` will be injected as a formal argument to other test case written that provides the opportunity 
to run each test cases individually. In unitttest everything is passed as self and the resource setup in the beginning.

```python
@pytest.fixture
def phonebook(tmpdir):
    """Provides an empty Phonebook"""
    return Phonebook(tmpdir)
```

However, we need to inject them for each test cases written here with as an argument passed in the test 
cases. In this case the `phonebook` is a dependency. 

```python
def test_lookup_by_name(phonebook):
    phonebook.add("Bob", "1234")
    assert "1234" == phonebook.lookup("Bob")
```

The name of the function under this decorator should be same as the argument passed in the other test cases
otherwise the tests will fail. 

```python
@pytest.fixture
def phonebook_typo(tmpdir): # This will be an error
    """Provides an empty Phonebook"""
    return Phonebook(tmpdir)
```

The tmpdir is another fixture that PyTest uses internally. This is passed as a argument to the phonebook
fixture. We can say it like fixture in fixture. The details of available fixtures can be seen here by 
command `pytest1>python.exe -m pytest --fixtures`

```text
tmpdir_factory [session scope] -- ...\_pytest\legacypath.py:295
    Return a :class:`pytest.TempdirFactory` instance for the test session.

tmpdir -- ...\_pytest\legacypath.py:302
    Return a temporary directory path object which is unique to each test
    function invocation, created as a sub directory of the base temporary
    directory.

caplog -- ...\_pytest\logging.py:487
    Access and control log capturing.


and many more. 
```

This `tmpdir` is giving or injecting an option to `PhoneBook` class to use it for storing the dictionary
inside it and use it without saving it. The `tmdir` is passed to `cache_directory` here.  

```python
    def __init__(self, cache_directory):
        self.numbers = {}
        self.filename = os.path.join(cache_directory, "phonebook.txt")
        self.cache = open(self.filename, "w")
```

Once the work is done PyTest will clear that tmpdir similar way Test-Fixtures works to clean up the mess
or resources.

If we run this command `pytest1>python.exe -m pytest --fixtures` at the very bottom we can see that the 
documentation is missing for phonebook fixture, because now it is a registered fixture for PyTest. 

So we need to add the documentation here `"""Provides an empty Phonebook"""` which will reflect 

```python
@pytest.fixture
def phonebook(tmpdir):
    """Provides an empty Phonebook"""
    return Phonebook(tmpdir)
```

```text
tmp_path -- ...\_pytest\tmpdir.py:199
    Return a temporary directory path object which is unique to each test
    function invocation, created as a sub directory of the base temporary
    directory.


--------------------------------------------------------- fixtures defined from test_phonebook ---------------------------------------------------------- 
phonebook -- test_phonebook.py:7
    Provides an empty Phonebook

```