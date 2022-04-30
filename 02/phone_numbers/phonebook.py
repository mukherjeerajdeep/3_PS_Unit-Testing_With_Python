class PhoneBook:
    def __init__(self):
        self.numbers = {}

    def add(self, name, number):
        self.numbers[name] = number

    def lookup(self, name):
        return self.numbers[name]

    # {
    #   "Bob": 12345,
    #   "Anna": 45678,
    #   "Tom": 123
    #  }
    #
    #  So Bob will be compared with Bob,Anna,Tom and then Anna will be with Bob,Anna,Tom.
    #  If name matches we continue because we are not checking names but if numbers first
    #  few digits matches with the other number then it should fail.
    def is_consistent(self):
        for name1, number1 in self.numbers.items():
            for name2, number2 in self.numbers.items():
                if name1 == name2:
                    continue
                if number1.startswith(number2):
                    return False
        return True

    def get_names(self):
        return self.numbers.keys()

    def get_numbers(self):
        return self.numbers.values()


