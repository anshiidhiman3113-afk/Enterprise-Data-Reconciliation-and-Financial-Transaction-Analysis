"""
main.py
-------------------------------------------------------
Enterprise Data Reconciliation Pipeline

Author: Anshika Dhiman
Project: Enterprise Data Reconciliation
Internship: iStudio Data Analytics Internship

Pipeline
--------
1. Extract transactions from server logs
2. Clean transaction records
3. Apply exchange rates
4. Reconcile customer database
5. Generate analytics
6. Export final outputs
"""

import os
import pandas as pd

from extract_logs import LogExtractor
from exchange_rate import ExchangeRateConverter
from reconciliation import EnterpriseReconciliation
from visualization import DataVisualizer


class EnterprisePipeline:

    def __init__(self):

        self.log_file = "../data/server_logs.txt"

        self.exchange_rate_file = "../data/daily_exchange_rates.csv"

        self.database_file = "../data/enterprise_database.db"

        self.output_folder = "../output"

        os.makedirs(self.output_folder, exist_ok=True)

    def extract_stage(self):

        print("\n====================================")
        print("STEP 1 : Extracting Server Logs")
        print("====================================")

        extractor = LogExtractor(self.log_file)

        transactions = extractor.clean()

        transactions.to_csv(
            f"{self.output_folder}/cleaned_transactions.csv",
            index=False
        )

        print(f"Transactions Extracted : {len(transactions)}")

        return transactions

    def exchange_rate_stage(self, transactions):

        print("\n====================================")
        print("STEP 2 : Currency Conversion")
        print("====================================")

        converter = ExchangeRateConverter(
            self.exchange_rate_file
        )

        converted = converter.convert_currency(
            transactions
        )

        converted.to_csv(
            f"{self.output_folder}/final_transactions.csv",
            index=False
        )

        print("Currency Conversion Completed.")

        return converted

    def reconciliation_stage(self, converted):

        print("\n====================================")
        print("STEP 3 : Customer Reconciliation")
        print("
