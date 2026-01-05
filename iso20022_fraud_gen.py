#!/usr/bin/env python3
"""
ISO 20022 Payment Fraud Data Generator
Generates synthetic transaction datasets with injected fraud patterns 
(ATO, Wire Fraud, Check Fraud) mapped to ISO 20022 standard fields.
"""

import pandas as pd
import numpy as np
from faker import Faker
import random
import uuid
from datetime import datetime, timedelta

# Initialize Faker and Seed for reproducibility
fake = Faker()
Faker.seed(42)
np.random.seed(42)

# --- CONFIGURATION ---
NUM_CUSTOMERS = 1000
NUM_TRANSACTIONS = 50000
FRAUD_RATIO = 0.05  # 5% fraud rate

class PaymentDataGenerator:
    def __init__(self, num_customers):
        self.customers = self._generate_customer_profiles(num_customers)
        self.fraudsters = self._generate_fraudster_profiles(int(num_customers * 0.1))

    def _generate_customer_profiles(self, n):
        profiles = []
        for _ in range(n):
            profiles.append({
                'Dbtr': fake.name(),            # Debtor (Sender) Name
                'DbtrAcct': fake.iban(),        # Debtor Account
                'DbtrAgt': fake.swift(),        # Debtor Agent (Bank BIC)
                'DbtrCtry': fake.country_code(),
                'AvgSpend': np.random.uniform(50, 500),
                'UsualDeviceID': str(uuid.uuid4())[:8],
                'UsualIP': fake.ipv4()
            })
        return pd.DataFrame(profiles)

    def _generate_fraudster_profiles(self, n):
        """External bad actors for specific fraud types like Wire/Check fraud"""
        profiles = []
        for _ in range(n):
            profiles.append({
                'Cdtr': fake.name(),            # Creditor (Receiver) Name
                'CdtrAcct': fake.iban(),
                'CdtrAgt': fake.swift(),
                'CdtrCtry': fake.country_code() if random.random() > 0.5 else 'RU', 
            })
        return pd.DataFrame(profiles)

    def generate_base_transaction(self, customer, is_fraud=False, fraud_type="None"):
        """Generates a single transaction row in ISO 20022 flavor"""
        
        # Base Data (Normal Behavior)
        txn_date = fake.date_time_between(start_date='-1y', end_date='now')
        amount = np.random.normal(customer['AvgSpend'], customer['AvgSpend'] * 0.2)
        amount = max(1.0, round(amount, 2))
        
        receiver = fake.company()
        receiver_acct = fake.iban()
        receiver_agt = fake.swift()
        
        device_id = customer['UsualDeviceID']
        ip_addr = customer['UsualIP']
        pmt_method = random.choice(['CreditCard', 'DebitCard', 'ACH', 'Wire'])

        # --- FRAUD INJECTION LOGIC ---
        if is_fraud:
            if fraud_type == "Credit/Debit Card Fraud":
                # CNP (Card Not Present): High amount, different IP, International Receiver
                amount = np.random.uniform(500, 2000) 
                ip_addr = fake.ipv4() 
                receiver_agt = fake.swift() 
                pmt_method = random.choice(['CreditCard', 'DebitCard'])

            elif fraud_type == "Account Takeover (ATO)":
                # High drain, new device, login from new IP
                amount = np.random.uniform(5000, 15000)
                device_id = str(uuid.uuid4())[:8] 
                ip_addr = fake.ipv4()