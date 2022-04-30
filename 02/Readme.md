# Phonebook and the tests 

Unittest can be directly invoked from command line with the command below. 
Remember that the unittest should be executed in the root directory where the 
tests resides. In this case it is from the phone numbers. 

![Directory Structure](C:\Users\erajmuk\Desktop\sstr.PNG)

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
`assertIn(member, container, msg=None) 
assertNotIn(member, container, msg=None)`