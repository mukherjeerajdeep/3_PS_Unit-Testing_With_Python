import unittest

from phonebook import PhoneBook


class PhoneBookTest(unittest.TestCase):

    # Setup and Teardown will run for each test cases
    def setUp(self) -> None:
        self.phonebook = PhoneBook()

    # Maybe needed when the resources are needed to be cleaned up,
    # here it is not needed.
    def tearDown(self) -> None:
        pass

    def test_lookup_by_name(self):
        self.phonebook.add("Bob", "12345")
        number = self.phonebook.lookup("Bob")
        self.assertEqual("12345", number)

    def test_missing_name(self):
        # We expect to get key error as the dictionary is empty
        # and hence it should return KeyError instead
        with self.assertRaises(KeyError):
            self.phonebook.lookup("missing")

    # @unittest.skip("WIP")
    def test_empty_phonebook_is_consistent(self):
        self.assertTrue(self.phonebook.is_consistent())

    # Bad test case writing where all the tests run together, and the
    # last one might not get executed because of the previous one is failed.
    # def test_is_consistent(self):
    #     self.phonebook.add("Bob", "12345")
    #     self.assertTrue(self.phonebook.is_consistent())
    #     self.phonebook.add("Anna", "43124")
    #     self.assertTrue(self.phonebook.is_consistent())
    #     self.phonebook.add("Tom", "12345")  # Identical entry to Bob
    #     self.assertTrue(self.phonebook.is_consistent())
    #     self.phonebook.add("Tom", "123")  # prefix of Bob
    #     self.assertTrue(self.phonebook.is_consistent())

    def test_is_consistent_with_different_entries(self):
        # given -> arrange
        self.phonebook.add("Bob", "12345")
        self.phonebook.add("Anna", "43124")
        # when -> act
        consistent = self.phonebook.is_consistent()
        # then -> assert
        self.assertTrue(consistent)

    def test_inconsistent_with_duplicate_entries(self):
        self.phonebook.add("Bob", "12345")
        self.phonebook.add("Tom", "12345")  # Identical entry to Bob
        self.assertFalse(self.phonebook.is_consistent())

    def test_inconsistent_with_duplicate_prefix(self):
        self.phonebook.add("Bob", "12345")
        self.phonebook.add("Tom", "123")  # prefix of Bob
        self.assertFalse(self.phonebook.is_consistent())