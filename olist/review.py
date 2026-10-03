import pandas as pd
import numpy as np
import math
from olist.data import Olist
from olist.order import Order


class Review:

    def __init__(self):
        # Import data only once
        olist = Olist()
        self.data = olist.get_data()
        self.order = Order()

    def get_review_length(self):
        """
        Returns a DataFrame with:
       'review_id', 'length_review', 'review_score'
        """
        order_reviews = self.data['order_reviews'].copy()


        order_reviews['length_review'] = order_reviews['review_comment_message'].str.len()

        return order_reviews[['review_id', 'length_review', 'review_score']]

    def get_main_product_category(self):
        """
        Returns a DataFrame with:
       'review_id', 'order_id','product_category_name'
        """

        order_reviews = self.data['order_reviews'].copy()
        order_items = self.data['order_items'].copy()
        products = self.data['products'].copy()

        order_reviews_order_items = order_reviews.merge(
            order_items,
            how = 'inner',
            on = 'order_id'
        )

        order_reviews_products = order_reviews_order_items.merge(
            products,
            how = 'inner',
            on = 'product_id'
        )

        return order_reviews_products[['review_id', 'order_id', 'product_category_name']]

    def get_training_data(self):
        """
        Returns a clean DataFrame (without NaN), merging review data
        with order data and product category.
        """
        # 1. Yorum uzunluğu ve puanı
        review_length = self.get_review_length()

        # 2. Ana ürün kategorisi
        main_category = self.get_main_product_category()

        # 3. Order verisini al (distance olmadan)
        order_data = self.order.get_training_data(with_distance_seller_customer=False)

        # 4. order_data'daki review_score'u çıkar (zaten review_length'de var)
        order_data = order_data.drop(columns=['review_score'])

        # 5. Yorum + kategori birleştir (review_id üzerinden)
        df = review_length.merge(
            main_category,
            on='review_id',
            how='inner'
        )

        # 6. Sonuç ile order verisini birleştir (order_id üzerinden)
        df = df.merge(
            order_data,
            on='order_id',
            how='inner'
        )

        # 7. NaN temizle
        df = df.dropna()

        return df
