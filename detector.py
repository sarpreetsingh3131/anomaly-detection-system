from customer import Customer


class Detector:

    def __init__(self, customers, logging, global_mean, global_std):
        self.customers = customers
        self.logging = logging
        self.global_mean = global_mean
        self.global_std = global_std

    def detect_anomaly(self, customer_id, merchant_id, transaction_amount):
        # ignore negative or 0 amount
        if transaction_amount < 1:
            return

        # check if customer already exists
        customer = self.customers.get(customer_id, None)

        if customer is None:
            # create a new customer and save it
            customer = Customer(id=customer_id, transactions=[])
            self.customers.__setitem__(customer_id, customer)

        # use global mean/std until customer has < 10 transactions
        if len(customer.transactions) < 10:
            mean = self.global_mean
            std = self.global_std
        else:
            mean = customer.get_mean()
            std = customer.get_std()

        max_allowed_amount = mean + 3 * std

        if transaction_amount > max_allowed_amount:
            self.logging.warning({
                'customer_id': customer_id,
                'merchant_id': merchant_id,
                'transaction_amount': transaction_amount,
                'max_allowed_amount': max_allowed_amount,
                'prev_3_transactions': customer.transactions[-3:]
            })

        customer.add_transaction(amount=transaction_amount)

        print('new transaction', {
            'customer_id': customer_id,
            'merchant_id': merchant_id,
            'amount': transaction_amount
        })
