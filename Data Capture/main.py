import faker
import psycopg2
import random 
from datetime import datetime

fake = faker.Faker()

def generate_transaction():
    user = fake.simple_profile()

    return {
        "transaction_id": fake.uuid4(),
        "user_id": user["user_id"],
        "timestamp": datetime.utcnow().timestamp(),
        "amount": round(random.uniform(10, 1000), 2),
        "currency": random.choice(["USD", "GBP"]),
        "city": fake.city(),
        "country": fake.country(),
        "merchant": fake.company(),
        "payment_method": random.choice(["credit_card", "debit_card", "bank_transfer", "paypal", "other"]),
        "ip_address": fake.ipv4(),
        "voucher_code": random.choice(['', 'DISCOUNT10']),
        "affiliate_id": fake.uuid4()
    }

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id VARCHAR(255) PRIMARY KEY,
            user_id VARCHAR(255),
            timestamp TIMESTAMP,
            amount DECIMAL,
            currency VARCHAR(3),
            city VARCHAR(100),
            country VARCHAR(100),
            merchant VARCHAR(100),
            payment_method VARCHAR(50),
            ip_address VARCHAR(50),
            voucher_code VARCHAR(50),
            affiliate_id VARCHAR(255)
        """
    )

    cursor.close()
    conn.commit()

if __name__ == "__main__":
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="financial_db",
        user="postgres",
        password="postgres"
    )
    create_table(conn)
    transction = generate_transaction()
    cur = conn.cursor()
    print(transction)
    cur.execute(
        """
        INSERT INTO transactions (transaction_id, user_id, timestamp, amount, currency, city, country, merchant, payment_method, ip_address, voucher_code, affiliate_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            transction["transaction_id"], 
            transction["user_id"], 
            datetime.fromtimestamp(transction["timestamp"]).strftime("%Y-%m-%d %H:%M:%S"), 
            transction["amount"], 
            transction["currency"], 
            transction["city"], 
            transction["country"], 
            transction["merchant"], 
            transction["payment_method"], 
            transction["ip_address"], 
            transction["voucher_code"], 
            transction["affiliate_id"]
        )
    )
    cur.close()
    conn.commit()