from olist.review import Review

r = Review()

# --- get_review_length testi ---
df = r.get_review_length()
print("--- REVIEW LENGTH ---")
print(df.head())
print(f"\nToplam satır: {len(df)}")
print(f"Sütunlar: {df.columns.tolist()}")
print(f"Ortalama yorum uzunluğu: {df['length_review'].mean():.1f} karakter")

# --- get_main_product_category testi ---
df2 = r.get_main_product_category()
print("\n--- MAIN PRODUCT CATEGORY ---")
print(df2.head())
print(f"\nToplam satır: {len(df2)}")
print(f"Sütunlar: {df2.columns.tolist()}")
print(f"Duplicate review_id sayısı: {df2['review_id'].duplicated().sum()}")

# --- get_training_data testi (henüz yazmadıysan yorum satırına al) ---
df3 = r.get_training_data()
print("\n--- TRAINING DATA ---")
print(df3.head())
print(f"\nToplam satır: {len(df3)}")
print(f"Sütunlar: {df3.columns.tolist()}")
