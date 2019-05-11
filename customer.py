import statistics

# simple class to hold customer info


class Customer:

    def __init__(self, id, transactions):
        self.id = id
        self.transactions = transactions

    def add_transaction(self, amount):
        if amount <= 0:
            raise ValueError('transaction is < 1')
        self.transactions.append(amount)

    def get_min_transaction(self):
        return min(self.transactions)

    def get_max_transaction(self):
        return max(self.transactions)

    def get_mean(self):
        return statistics.mean(data=self.transactions)

    def get_std(self):
        return statistics.stdev(data=self.transactions)

    def get_ratio(self, amount):
        return amount / self.get_min_transaction()

