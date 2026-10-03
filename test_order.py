# test_order.py
import sys
from olist.order import Order

o = Order()

# Test etmek istediğin metodu komut satırından seç
# Kullanım: python test_order.py wait_time
#          python test_order.py review_score
#          python test_order.py number_items
#          python test_order.py number_sellers
#          python test_order.py price_freight

if len(sys.argv) < 2:
    print("Kullanım: python test_order.py <metod_adi>")
    print("Örnek: python test_order.py wait_time")
    sys.exit(1)

metod = sys.argv[1]

if metod == "wait_time":
    print(o.get_wait_time().head())
elif metod == "review_score":
    print(o.get_review_score().head())
elif metod == "number_items":
    print(o.get_number_items().head())
elif metod == "number_sellers":
    print(o.get_number_sellers().head())
elif metod == "price_freight":
    print(o.get_price_and_freight().head())
elif metod == "distance":
    df = o.get_distance_seller_customer()
    print(df.head())
    print(f"\nToplam satır: {len(df)}")
    print(f"Ortalama mesafe (km): {df['distance_seller_customer'].mean():.2f}")
    print(f"Maksimum mesafe (km): {df['distance_seller_customer'].max():.2f}")
elif metod == "training_data":
    df = o.get_training_data()
    print(df.head())
    print(f"\nToplam satır: {len(df)}")
    print(f"Sütunlar: {df.columns.tolist()}")

elif metod == "training_data_with_distance":
    df = o.get_training_data(with_distance_seller_customer=True)
    print(df.head())
    print(f"\nToplam satır: {len(df)}")
    print(f"Sütunlar: {df.columns.tolist()}")

else:
    print(f"Bilinmeyen metot: {metod}")
