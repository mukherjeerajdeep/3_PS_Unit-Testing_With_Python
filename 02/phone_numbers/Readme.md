# Phonebook and the tests 

Unittest can be directly invoked from command line with the command below. 
Remember that the unittest should be executed in the root directory where the 
tests reside. In this case it is from the phone numbers. 

Test can be executed from the command line or from the test runner from PyCharm. 
Add Config -> Select the Unittest -> Select the folder/file to run 

```text
PS ...\02\phone_numbers> python.exe -m unittest 
.......
----------------------------------------------------------------------
Ran 7 tests in 0.001s

OK
```

Here is the URL for the large phonebook to do load test for the test scrips.
[GitHub Repo for Phone Numbers](https://github.com/emilybache/Phone-Numbers-Kata)

## Check the methods of the test cases we can use 

[Test cases](https://docs.python.org/3/library/unittest.html#test-cases)

[Check Description in assertIn](https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertIn)

is member contained in the container ? True if yes. container can be an iterable

* assertIn(member, container, msg=None) 
* assertNotIn(member, container, msg=None)

A Test can be skipped by the following decorators.    
```python
    # @unittest.skip("WIP")
    def test_empty_phonebook_is_consistent(self):
        self.assertTrue(self.phonebook.is_consistent())
```

The test fixtures used in the unittest is with overriding the default methods `setup()` amd `teardown()`. Both should be available when overridden.
![override](https://user-images.githubusercontent.com/43293317/167314199-5b07700b-962c-42d5-9aa9-1374a6e37611.PNG)

```python
    # Setup and Teardown will run for each test cases
    def setUp(self) -> None:
        self.phonebook = PhoneBook()

    # Maybe needed when the resources are needed to be cleaned up,
    # here it is not needed.
    def tearDown(self) -> None:
        pass
```

Asserting the Exceptions can be done in this way, the use of context-managers and then execute the callable that would raise the exception.

```python
    def test_missing_name(self):
        # We expect to get key error as the dictionary is empty
        # and hence it should return KeyError instead
        with self.assertRaises(KeyError):
            self.phonebook.lookup("missing")
```

## Test Execution Hierarchy

Each test-cases should be executed in this following manner.
setup() -> Run TC() -> teardown() -- This is the way the tests should always run.
So whatever happens in the Run TC() stage the teardown() should always be executed. 


However, in case the setup() is not executed then neither the test-cases() nor the teardown() will be executed because teardown() is supposed to release the resources which are not even created because the setup() was not even executed. 

## Four vocabulary 

* Test Case 
* Test Suite
* Test Fixture 
* Test Runner 

## Breaking down into smaller test cases.

Writing the bad TC's are as example below, rather break it down into smaller and cohesive test cases. 
```python
    def test_is_consistent(self):
        self.phonebook.add("Bob", "12345")
        self.assertTrue(self.phonebook.is_consistent())
        self.phonebook.add("Anna", "43124")
        self.assertTrue(self.phonebook.is_consistent())
        self.phonebook.add("Tom", "12345")  # Identical entry to Bob
        self.assertTrue(self.phonebook.is_consistent())  <-- It fails here and the rest would not be executed
        self.phonebook.add("Tom", "123")  # prefix of Bob
        self.assertTrue(self.phonebook.is_consistent())
```

For example the take-out the first two conditions and assert them with meaningful test names with purpose. 
#### **Pythonic way of testing** 
Arrange -> Act -> Assert

```python
    def test_is_consistent_with_different_entries(self):
        # given -> arrange
        self.phonebook.add("Bob", "12345")
        self.phonebook.add("Anna", "43124")
        # when -> act
        consistent = self.phonebook.is_consistent()
        # then -> assert
        self.assertTrue(consistent)
```



