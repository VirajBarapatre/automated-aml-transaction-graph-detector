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