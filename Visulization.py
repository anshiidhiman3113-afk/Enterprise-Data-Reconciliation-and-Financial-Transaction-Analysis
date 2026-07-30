"""
visualization.py
-------------------------------------------------------
Enterprise Data Reconciliation Project

Creates analytical charts and exports them to the output folder.

Charts:
1. Daily Transaction Trend
2. Revenue Distribution
3. Top Products
4. Top Customers
"""

import os
import pandas as pd
import matplotlib.pyplot as plt


class DataVisualizer:

    def __init__(self, dataframe):

        self.df = dataframe

    def create_output_folder(self):

        os.makedirs("../output", exist_ok=True)

    def transaction_trend(self):

        trend = (

            self.df.groupby("transaction_date")["usd_amount"]

            .sum()

            .sort_index()

        )

        plt.figure(figsize=(12, 6))

        plt.plot(
            trend.index,
            trend.values,
            linewidth=2
       
