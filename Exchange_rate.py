"""
exchange_rate.py
-------------------------------------------------------
Handles enterprise exchange-rate reconciliation.

Features
--------
✔ Load daily exchange rates
✔ Handle missing weekend values using forward-fill
✔ Merge with transaction dataset
✔ Convert EUR to USD
✔ Export final dataset
"""

import pandas as pd


class ExchangeRateConverter:

    def __init__(self, exchange_rate_file):

        self.exchange_rate_file = exchange_rate_file

    def load_exchange_rates(self):

        rates = pd.read_csv(self.exchange_rate_file)

        rates["date"] = pd.to_datetime(rates["date"])

        rates = rates.sort_values("date")

        return rates

    def prepare_rates(self):

        rates = self.load_exchange_rates()

        full_dates = pd.date_range(
            start=rates["date"].min(),
            end=rates["date"].max(),
            freq="D"
        )

        rates = (
            rates
            .set_index("date")
            .reindex(full_dates)
            .rename_axis("date")
            .reset_index()
        )

        # Fill weekend exchange rates
        rates["exchange_rate"] = (
            rates["exchange_rate"]
            .ffill()
        )

        return rates

    def convert_currency(self, transactions):

        rates = self.prepare_rates()

        transactions["transaction_date"] = pd.to_datetime(
            transactions["transaction_date"]
        ).dt.normalize()

        merged = transactions.merge(
            rates,
            left_on="transaction_date",
            right_on="date",
            how="left"
        )

        merged["exchange_rate"] = (
            merged["exchange_rate"]
            .ffill()
        )

        merged["usd_amount"] = (
            merged["eur_amount"]
            * merged["exchange_rate"]
        ).round(2)

        merged.drop(columns=["date"], inplace=True)

        return merged

    def export(self, transactions, output_path):

        final_df = self.convert_currency(transactions)

        final_df.to_csv(
            output_path,
            index=False
        )

        print(
            f"Currency conversion completed. "
            f"{len(final_df)} records exported."
        )

        return final_df


if __name__ == "__main__":

    # Example usage

    transactions = pd.read_csv(
        "../output/cleaned_transactions.csv"
    )

    converter = ExchangeRateConverter(
        "../data/daily_exchange_rates.csv"
    )

    converter.export(
        transactions,
        "../output/final_transactions.csv"
  )
