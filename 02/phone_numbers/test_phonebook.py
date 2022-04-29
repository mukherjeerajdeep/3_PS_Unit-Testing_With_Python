import unittest

from phonebook import PhoneBook


class PhoneBookTest(unittest.TestCase):

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

    @unittest.skip("WIP")
    def test_empty_phonebook_is_consistent(self):
        self.assertTrue(self.phonebook.is_consistent())
