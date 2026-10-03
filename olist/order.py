import pandas as pd
import numpy as np
from olist.utils import haversine_distance
from olist.data import Olist


class Order:
    '''
    DataFrames containing all orders as index,
    and various properties of these orders as columns
    '''
    def __init__(self):
        # Assign an attribute ".data" to all new instances of Order
        self.data = Olist().get_data()

    def get_wait_time(self, is_delivered=True):
        """
        Returns a DataFrame with:
        [order_id, wait_time, expected_wait_time, delay_vs_expected, order_status]
        and filters out non-delivered orders unless specified
        """
        # Hint: Within this instance method, you have access to the instance of the class Order in the variable self, as well as all its attributes

        orders = self.data['orders'].copy()

        if is_delivered:
            orders = orders[orders['order_status'] == 'delivered']

        date_columns = [
            'order_purchase_timestamp',
            'order_delivered_customer_date',
            'order_estimated_delivery_date'
        ]

        for col in date_columns:
            orders[col] = pd.to_datetime(orders[col])

        orders['wait_time'] = (orders['order_delivered_customer_date'] - orders['order_purchase_timestamp']).dt.days
        orders['expected_wait_time'] = (orders['order_estimated_delivery_date'] - orders['order_purchase_timestamp']).dt.days
        orders['delay_vs_expected'] = (orders['order_delivered_customer_date'] - orders['order_estimated_delivery_date']).dt.days

        result = orders[['order_id', 'wait_time', 'expected_wait_time', 'delay_vs_expected', 'order_status']]

        return result

    def get_review_score(self):
        """
        Returns a DataFrame with:
        order_id, dim_is_five_star, dim_is_one_star, review_score
        """
        reviews = self.data['order_reviews'].copy()

        reviews['dim_is_five_star'] = (reviews['review_score'] == 5).astype(int)
        reviews['dim_is_one_star'] = (reviews['review_score'] == 1).astype(int)

        return reviews[['order_id', 'dim_is_five_star', 'dim_is_one_star', 'review_score']]


    def get_number_items(self):
        order_items = self.data['order_items'].copy()


        number_of_items = order_items.groupby('order_id')['order_item_id'].count().reset_index()

        number_of_items.columns = ['order_id', 'number_of_items']

        return number_of_items

    def get_number_sellers(self):
        """
        Returns a DataFrame with:
        order_id, number_of_sellers
        """
        order_items = self.data['order_items'].copy()

        number_of_sellers = order_items.groupby('order_id')['seller_id'].nunique().reset_index()

        number_of_sellers.columns = ['order_id', 'number_of_sellers']

        return number_of_sellers



    def get_price_and_freight(self):
        """
        Returns a DataFrame with:
        order_id, price, freight_value
        """

        order_items = self.data['order_items'].copy()

        price_and_freight = order_items.groupby('order_id')[['price', 'freight_value']].sum().reset_index()

        return price_and_freight

    # Optional
    def get_distance_seller_customer(self):

        orders = self.data['orders'].copy()
        order_items = self.data['order_items'].copy()
        customers = self.data['customers'].copy()
        sellers = self.data['sellers'].copy()
        geo = self.data['geolocation'].copy()

        geo = geo.groupby('geolocation_zip_code_prefix')[['geolocation_lat', 'geolocation_lng']].mean().reset_index()

        orders_customers = orders.merge(customers, on = 'customer_id', how = 'inner')

        orders_customers = orders_customers.merge(
            geo,
            left_on = 'customer_zip_code_prefix',
            right_on = 'geolocation_zip_code_prefix',
            how = 'inner'
        )

        orders_customers = orders_customers.rename(columns = {
            'geolocation_lat': 'customer_lat',
            'geolocation_lng': 'customer_lng'
        })

        items_sellers = order_items.merge(sellers, on='seller_id', how='inner')

        items_sellers = items_sellers.merge(
            geo,
            left_on='seller_zip_code_prefix',
            right_on='geolocation_zip_code_prefix',
            how = 'inner'
        )

        items_sellers = items_sellers.rename(columns={
            'geolocation_lat': 'seller_lat',
            'geolocation_lng': 'seller_lng'
        })

        df = items_sellers.merge(
            orders_customers[['order_id', 'customer_lat', 'customer_lng']],
            on = 'order_id',
            how = 'inner'
        )

        df['distance_seller_customer'] = df.apply(
            lambda row: haversine_distance(
                row['seller_lng'], row['seller_lat'],
                row['customer_lng'], row['customer_lat']
            ), axis = 1
        )

        result = df.groupby('order_id')['distance_seller_customer'].mean().reset_index()

        return result

    def get_training_data(self,
                          is_delivered=True,
                          with_distance_seller_customer=False):
        """
        Returns a clean DataFrame (without NaN), with the all following columns:
        ['order_id', 'wait_time', 'expected_wait_time', 'delay_vs_expected',
        'order_status', 'dim_is_five_star', 'dim_is_one_star', 'review_score',
        'number_of_items', 'number_of_sellers', 'price', 'freight_value',
        'distance_seller_customer']
        """
        # Hint: make sure to re-use your instance methods defined above

        wait_time = self.get_wait_time(is_delivered)
        review_score = self.get_review_score()
        number_items = self.get_number_items()
        number_sellers = self.get_number_sellers()
        price_freight = self.get_price_and_freight()

        df = wait_time.merge(review_score, on='order_id', how='inner')
        df = df.merge(number_items, on='order_id', how='inner')
        df = df.merge(number_sellers, on='order_id', how='inner')
        df = df.merge(price_freight, on='order_id', how='inner')

        if with_distance_seller_customer:
            distance = self.get_distance_seller_customer()
            df = df.merge(distance, on='order_id', how='inner')

        df = df.dropna()

        return df
