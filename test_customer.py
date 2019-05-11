import unittest
from customer import Customer


class TestCustomer(unittest.TestCase):

    def setUp(self):
        self.sut = Customer(id='1', transactions=[])
        self.transactions = [i for i in range(1, 1000)]
        self.add_transactions()

    def test_should_add_transactions(self):
        self.assertEqual(self.sut.transactions, self.transactions)

    def test_should_return_min_transaction(self):
        self.assertEqual(self.sut.get_min_transaction(), min(self.transactions))

    def test_should_return_max_transaction(self):
        self.assertEqual(self.sut.get_max_transaction(), max(self.transactions))

    def test_should_return_mean(self):
        self.assertEqual(self.sut.get_max_transaction(), max(self.transactions))

    def test_should_return_std(self):
        self.assertEqual(self.sut.get_max_transaction(), max(self.transactions))

    def test_should_return_ratio(self):
        self.assertEqual(self.sut.get_ratio(amount=10), 10 / min(self.transactions))

    def test_should_not_add_negative_transactions(self):
        for amount in range(1000):
            self.assertRaises(ValueError, self.sut.add_transaction, amount=-amount)

    # when no transaction is made
    def test_should_not_return_min_transaction(self):
        self.sut.transactions = []
        self.assertRaises(ValueError, self.sut.get_min_transaction)

    def test_should_not_return_max_transaction(self):
        self.sut.transactions = []
        self.assertRaises(ValueError, self.sut.get_max_transaction)

    def test_should_not_return_mean(self):
        self.sut.transactions = []
        self.assertRaises(ValueError, self.sut.get_mean)

    def test_should_not_return_std(self):
        self.sut.transactions = []
        self.assertRaises(ValueError, self.sut.get_std)

    def test_should_not_return_ration(self):
        self.sut.transactions = []
        self.assertRaises(ValueError, self.sut.get_ratio, 10)

    def add_transactions(self):
        for amount in self.transactions:
            self.sut.add_transaction(amount=amount)
