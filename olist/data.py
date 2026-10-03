from pathlib import Path
import pandas as pd

DATA_PATH = Path.home() / ".workintech" / "olist" / "data" / "csv"


class Olist:
    """
    The Olist class provides methods to interact with Olist's e-commerce data.

    Methods:
        get_data():
            Loads and returns a dictionary where keys are dataset names (e.g., 'sellers', 'orders')
            and values are pandas DataFrames loaded from corresponding CSV files.

        ping():
            Prints "pong" to confirm the method is callable.
    """

    def __init__(self):
        self.data_path = DATA_PATH


    def get_data(self):
        """
        This function returns a Python dict.
        Its keys should be 'sellers', 'orders', 'order_items' etc...
        Its values should be pandas.DataFrames loaded from csv files
        """
        data = {
            "customers": pd.read_csv(self.data_path / "olist_customers_dataset.csv"),
            "geolocation": pd.read_csv(self.data_path / "olist_geolocation_dataset.csv"),
            "order_items": pd.read_csv(self.data_path / "olist_order_items_dataset.csv"),
            "order_payments": pd.read_csv(self.data_path / "olist_order_payments_dataset.csv"),
            "order_reviews": pd.read_csv(self.data_path / "olist_order_reviews_dataset.csv"),
            "orders": pd.read_csv(self.data_path / "olist_orders_dataset.csv"),
            "products": pd.read_csv(self.data_path / "olist_products_dataset.csv"),
            "sellers": pd.read_csv(self.data_path / "olist_sellers_dataset.csv"),
            "product_category_name_translation": pd.read_csv(self.data_path / "product_category_name_translation.csv")
        }

        return data

    def ping(self):
        """
        You call ping I print pong.
        """
        return "pong"
