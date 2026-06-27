import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random

fake = Faker()

def generate_sales_data(n_records=10000):
    categories = ['Electronics', 'Clothing', 'Food', 'Books', 'Sports']
    regions = ['Cairo', 'Alexandria', 'Giza', 'Luxor', 'Aswan']
    
    data = []
    start_date = datetime(2022, 1, 1)
    
    for i in range(n_records):
        date = start_date + timedelta(days=random.randint(0, 730))
        category = random.choice(categories)
        region = random.choice(regions)
        quantity = random.randint(1, 50)
        price = round(random.uniform(10, 500), 2)
        discount = round(random.uniform(0, 0.3), 2)
        revenue = round(quantity * price * (1 - discount), 2)
        
        data.append({
            'date': date.strftime('%Y-%m-%d'),
            'category': category,
            'region': region,
            'quantity': quantity,
            'price': price,
            'discount': discount,
            'revenue': revenue,
            'customer_id': fake.uuid4()
        })
    
    df = pd.DataFrame(data)
    df.to_csv('data/sales_data.csv', index=False)
    print(f"Generated {n_records} records successfully!")
    return df

if __name__ == "__main__":
    df = generate_sales_data()
    print(df.head())
    print(f"Shape: {df.shape}")