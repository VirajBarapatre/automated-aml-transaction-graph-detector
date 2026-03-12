import sqlite3

# Connect to (or create) the database file
conn = sqlite3.connect('aml_system.db')
cursor = conn.cursor()

# 1. Create the Users table (KYC data)
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    name TEXT,
    risk_level TEXT, -- 'Low', 'Medium', 'High' (e.g. PEPs)
    country_code TEXT
)
''')

# 2. Create the Transactions table
cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    txn_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER,
    receiver_id INTEGER,
    amount REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    method TEXT, -- 'Wire', 'Cash', 'Crypto'
    FOREIGN KEY (sender_id) REFERENCES users(user_id)
)
''')

conn.commit()
print("Database and AML tables created successfully!")

import sqlite3
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

conn = sqlite3.connect('aml_system.db')

# 1. Create 500 Random Users
users = []
for i in range(1, 501):
    risk = random.choices(['Low', 'Medium', 'High'], weights=[80, 15, 5])[0]
    users.append((i, f"User_{i}", risk, random.choice(['US', 'GB', 'KY', 'LU', 'CH'])))

conn.executemany("INSERT INTO users VALUES (?, ?, ?, ?)", users)

# 2. Generate 9,900 Normal Transactions
txns = []
for _ in range(9900):
    s, r = random.sample(range(1, 501), 2)
    amt = round(random.uniform(10, 2000), 2)
    txns.append((s, r, amt, 'Wire'))

# 3. Inject 100 "Anomalous" Transactions (The Money Launderers)
# Pattern: "Structuring" - many transactions just under $10k
for _ in range(50):
    s, r = 99, 100 # A specific pair
    amt = round(random.uniform(9000, 9999), 2) 
    txns.append((s, r, amt, 'Cash'))

# Pattern: "Rapid Outflow" - One huge sum split instantly
for _ in range(50):
    s = 400
    r = random.randint(1, 50)
    amt = 50000.00
    txns.append((s, r, amt, 'Crypto'))

conn.executemany("INSERT INTO transactions (sender_id, receiver_id, amount, method) VALUES (?, ?, ?, ?)", txns)
conn.commit()
print("Data Injection Complete: 10,000 records added.")