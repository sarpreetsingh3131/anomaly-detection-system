import unittest
from unittest.mock import MagicMock
from detector import Detector


class TestDetector(unittest.TestCase):

    def setUp(self):
        self.mock_customers = MagicMock()
        self.mock_logging = MagicMock()
        self.mock_customer = MagicMock()
        self.global_mean = 100
        self.global_std = 100
        self.sut = Detector(
            customers=self.mock_customers,
            logging=self.mock_logging,
            global_mean=self.global_mean,
            global_std=self.global_std
        )
        self.mock_customers.return_value.get = self.mock_customer

    def test_should_ignore_invalid_transaction(self):
        self.sut.detect_anomaly(customer_id='1', merchant_id='1', transaction_amount=0)
        self.sut.detect_anomaly(customer_id='1', merchant_id='1', transaction_amount=-10)
        assert not self.mock_customers.get.called

    def test_should_detect_anomaly_with_global_statistics(self):
        transaction_amount = (self.global_mean + 3 * self.global_std) + 1
        self.sut.detect_anomaly(customer_id='1', merchant_id='1', transaction_amount=transaction_amount)
        self.verify_assert(detect=True)

    def test_should_not_detect_anomaly_with_global_statistics(self):
        transaction_amount = (self.global_mean + 3 * self.global_std)
        self.sut.detect_anomaly(customer_id='1', merchant_id='1', transaction_amount=transaction_amount)
        self.verify_assert(detect=False)

    def test_should_detect_anomaly(self):
        mean = 10
        std = 10
        transaction_amount = (mean + 3 * std) + 1
        self.mock_customer.return_value.transactions = [1 for _ in range(1, 11)]
        self.mock_customer.return_value.get_mean = mean
        self.mock_customer.return_value.get_std = std
        self.sut.detect_anomaly(customer_id='1', merchant_id='1', transaction_amount=transaction_amount)
        self.verify_assert(detect=True)

    def test_should_not_detect_anomaly(self):
        mean = 11
        std = 11
        transaction_amount = (mean + 3 * std)
        self.mock_customer.return_value.transactions = [1 for _ in range(1, 11)]
        self.mock_customer.return_value.get_mean = mean
        self.mock_customer.return_value.get_std = std
        self.sut.detect_anomaly(customer_id='1', merchant_id='1', transaction_amount=transaction_amount)
        self.verify_assert(detect=False)

    def verify_assert(self, detect):
        if detect:
            assert self.mock_customers.get.assert_called_once
            assert self.mock_customers.__setitem__.assert_called_once
            assert self.mock_logging.warning.assert_called_once
            assert self.mock_logging.customer.add_transaction.assert_called_once
        else:
            assert self.mock_customers.get.assert_called_once
            assert self.mock_customers.__setitem__.assert_called_once
            assert not self.mock_logging.warning.called
            assert self.mock_logging.customer.add_transaction.assert_called_once
