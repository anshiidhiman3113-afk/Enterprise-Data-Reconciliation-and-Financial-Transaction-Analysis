"""
reconciliation.py
-------------------------------------------------------
Enterprise Customer Reconciliation

Features
--------
✔ Connects to SQLite database
✔ Retrieves latest customer record using SQL Window Function
✔ Merges customer information with transaction data
✔ Generates reconciliation statistics
✔ Exports final enterprise dataset
"""

import sqlite3
import pandas as pd


class EnterpriseReconciliation:

    def __init__(self, database_path):

        self.database_path = database_path

    def connect_database(self):

        return sqlite3.connect(self.database_path)

    def fetch_latest_customers(self):

        connection = self.connect_database()

        query = """

        WITH latest_customer AS (

            SELECT
                *,
                ROW_NUMBER() OVER(

                    PARTITION BY user_id
                    ORDER BY updated_at DESC

                ) AS rn

            FROM customers

        )

        SELECT *

        FROM latest_customer

        WHERE rn = 1;

        """

        customers = pd.read_sql_query(
            query,
            connection
        )

        connection.close()

        return customers

    def merge_transactions(
        self,
        transaction_df
    ):

        customer_df = self.fetch_latest_customers()

        merged = transaction_df.merge(

            customer_df,

            on="user_id",

            how="left"

        )

        return merged

    def reconciliation_summary(
        self,
        merged_df
    ):

        summary = {

            "Total Transactions":
                len(merged_df),

            "Matched Customers":
                merged_df["user_id"].count(),

            "Missing Customers":
                merged_df["customer_name"].isna().sum()
                if "customer_name" in merged_df.columns
                else 0,

            "Total Revenue (USD)":
                round(
                    merged_df["usd_amount"].sum(),
                    2
                )
                if "usd_amount" in merged_df.columns
                else 0,

            "Average Transaction":
                round(
                    merged_df["usd_amount"].mean(),
                    2
                )
                if "usd_amount" in merged_df.columns
                else 0,

            "Unique Customers":
                merged_df["user_id"].nunique()

        }

        return pd.DataFrame(

            summary.items(),

            columns
