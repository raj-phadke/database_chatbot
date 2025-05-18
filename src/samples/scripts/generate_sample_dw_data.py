import pandas as pd
import random
from datetime import datetime, timedelta


def generate_sample_data() -> None:
    # Set random seed for reproducibility
    random.seed(42)

    # Sample dimension data
    product_list = [
        (1, "Laptop", "Electronics", 999.99),
        (2, "Headphones", "Electronics", 199.99),
        (3, "Keyboard", "Electronics", 49.99),
        (4, "Coffee Maker", "Home Appliances", 79.99),
        (5, "Blender", "Home Appliances", 59.99),
    ]

    customer_list = [
        (101, "Alice", "Smith", "alice@example.com", "NY"),
        (102, "Bob", "Jones", "bob@example.com", "CA"),
        (103, "Charlie", "Brown", "charlie@example.com", "TX"),
        (104, "Diana", "Prince", "diana@example.com", "WA"),
        (105, "Ethan", "Hunt", "ethan@example.com", "FL"),
    ]

    store_list = [
        (10, "Tech Hub NYC", "New York", "NY"),
        (20, "Tech Hub SF", "San Francisco", "CA"),
        (30, "Home Goods Dallas", "Dallas", "TX"),
    ]

    # Generate dim_date
    start_date = datetime(2025, 1, 1)
    date_data = []
    for i in range(100):
        date = start_date + timedelta(days=i)
        date_data.append(
            {
                "date_key": date.date(),
                "day_of_week": date.strftime("%A"),
                "month": date.strftime("%B"),
                "quarter": f"Q{((date.month - 1) // 3) + 1}",
                "year": date.year,
            }
        )

    # Generate fact_sales
    fact_sales_data = []
    for sale_id in range(1001, 2001):
        date = random.choice(date_data)["date_key"]
        product = random.choice(product_list)
        customer = random.choice(customer_list)
        store = random.choice(store_list)
        quantity = random.randint(1, 5)
        total_amount = round(product[3] * quantity, 2)

        fact_sales_data.append(
            {
                "sale_id": sale_id,
                "date_key": date,
                "product_id": product[0],
                "customer_id": customer[0],
                "store_id": store[0],
                "quantity_sold": quantity,
                "total_amount": total_amount,
            }
        )

    # Convert to DataFrames
    df_dim_date = pd.DataFrame(date_data).drop_duplicates(subset="date_key")
    df_dim_product = pd.DataFrame(
        product_list, columns=["product_id", "product_name", "category", "price"]
    )
    df_dim_customer = pd.DataFrame(
        customer_list,
        columns=["customer_id", "first_name", "last_name", "email", "state"],
    )
    df_dim_store = pd.DataFrame(
        store_list, columns=["store_id", "store_name", "city", "state"]
    )
    df_fact_sales = pd.DataFrame(fact_sales_data)

    df_dict = {
        "dim_date": df_dim_date,
        "dim_product": df_dim_product,
        "dim_customer": df_dim_customer,
        "dim_store": df_dim_store,
        "fact_sales": df_fact_sales,
    }

    return df_dict
