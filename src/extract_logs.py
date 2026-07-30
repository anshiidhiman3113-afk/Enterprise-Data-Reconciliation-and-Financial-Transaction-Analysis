"""
extract_logs.py
----------------------------------------
Extracts transaction records from raw server logs.

Features
--------
✔ Regex-based parsing
✔ Ignores corrupted/error records
✔ Vectorized DataFrame creation
✔ Exports cleaned transactions
"""

import re
import pandas as pd


class LogExtractor:

    def __init__(self, logfile):
        self.logfile = logfile

    def read_logs(self):
        """Read all log lines."""
        with open(self.logfile, "r", encoding="utf-8") as file:
            return file.readlines()

    def extract_transactions(self):

        logs = self.read_logs()

        transactions = []

        pattern = re.compile(
            r"""
            \[(?P<date>.*?)\]          # Timestamp
            .*?
            payload=
            \{
            "user":"(?P<user>.*?)",
            "item_code":"(?P<product>.*?)",
            "eur_val":(?P<amount>[0-9.]+)
            \}
            """,
            re.VERBOSE,
        )

        for line in logs:

            match = pattern.search(line)

            if match:

                transactions.append(
                    {
                        "transaction_date": match.group("date"),
                        "user_id": match.group("user"),
                        "product_id": match.group("product"),
                        "eur_amount": float(match.group("amount")),
                    }
                )

        df = pd.DataFrame(transactions)

        return df

    def remove_duplicates(self, df):

        return df.drop_duplicates()

    def remove_missing(self, df):

        return df.dropna()

    def clean(self):

        df = self.extract_transactions()

        df = self.remove_duplicates(df)

        df = self.remove_missing(df)

        df["transaction_date"] = pd.to_datetime(
            df["transaction_date"]
        )

        return df

    def export(self, output_path):

        df = self.clean()

        df.to_csv(output_path, index=False)

        print(f"Saved {len(df)} records.")

        return df


if __name__ == "__main__":

    extractor = LogExtractor(
        "../data/server_logs.txt"
    )

    cleaned = extractor.export(
        "../output/cleaned_transactions.csv"
    )

    print(cleaned.head())
