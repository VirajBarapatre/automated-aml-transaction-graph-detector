import sqlite3
import pandas as pd

def extract_features():
    conn = sqlite3.connect('aml_system.db')
    
    # SQL Query to join transactions with user risk levels
    # We calculate: Total count, Total Volume, and Average transaction size
    query = """
    SELECT 
        u.user_id,
        u.risk_level,
        u.country_code,
        COUNT(t.txn_id) as txn_count,
        SUM(t.amount) as total_volume,
        AVG(t.amount) as avg_txn_amount
    FROM users u
    LEFT JOIN transactions t ON u.user_id = t.sender_id
    GROUP BY u.user_id
    """
    
    df = pd.read_sql_query(query, conn)
    
    # Feature Engineering: Convert Risk Level text to numbers
    risk_map = {'Low': 1, 'Medium': 2, 'High': 3}
    df['risk_score'] = df['risk_level'].map(risk_map)
    
    # Feature Engineering: Flag high-risk countries (Example: Cayman Islands 'KY')
    df['country_risk'] = df['country_code'].apply(lambda x: 5 if x in ['KY', 'LU'] else 1)
    
    conn.close()
    return df

if __name__ == "__main__":
    features = extract_features()
    print("Features extracted successfully!")
    print(features.head())