import pandas as pd
import numpy as np
from detector import Detector
import logging

"""
we can clean the data in following ways:
1. remove all the missing values rows
2. use some learning models to predict the missing values
3. fill the missing values:
    - take a missing value row, i.e., customer_id, merchant_id, transaction_amount
    - compute the mean of all the transactions that have same merchant_id and assign that value to the missing value
    - if merchant_id is not available, then go with customer_id

I choose the first way because the data is huge and even after removing the corrupted data, I am left with sufficient
amount of data
"""


dataset = pd.read_csv('data.csv', header=None, usecols=[0, 1, 2], dtype={0: str, 1: str})

# assign column names
dataset.columns = ['customer_id', 'merchant_id', 'transaction_amount']

dataset[['transaction_amount']] = dataset[['transaction_amount']].replace('X', np.NAN)

dataset.dropna(inplace=True)

# change transaction amount datatype to float
dataset['transaction_amount'] = dataset['transaction_amount'].astype(float)


logging.basicConfig(filename='fraud.log', filemode='w')

detector = Detector(
    customers={},
    logging=logging,
    global_mean=dataset['transaction_amount'].mean(),
    global_std=dataset['transaction_amount'].std()
)


for customer_id, merchant_id, transaction_amount in dataset.values:
    detector.detect_anomaly(
        customer_id=customer_id,
        merchant_id=merchant_id,
        transaction_amount=transaction_amount
    )
