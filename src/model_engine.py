import sqlite3
import pandas as pd
from sklearn.ensemble import IsolationForest
from feature_eng import extract_features # Importing your previous work!

def run_anomaly_detection():
    # 1. Get the features from your previous script
    df = extract_features()
    
    # 2. Select the numerical columns for the AI to analyze
    # We include our engineered risk scores
    model_features = ['txn_count', 'total_volume', 'avg_txn_amount', 'risk_score', 'country_risk']
    X = df[model_features]
    
    # 3. Initialize the Isolation Forest
    # contamination=0.03 means we want to flag the top 3% most suspicious users
    model = IsolationForest(contamination=0.03, random_state=42)
    
    # 4. Predict (-1 is an anomaly, 1 is normal)
    df['is_anomaly'] = model.fit_predict(X)
    
    # 5. Filter only the suspicious ones
    alerts = df[df['is_anomaly'] == -1].copy()
    
    # 6. Save these alerts back to the SQLite Database
    conn = sqlite3.connect('aml_system.db')
    alerts.to_sql('alerts', conn, if_exists='replace', index=False)
    conn.close()
    
    print(f"Detection complete! Found {len(alerts)} suspicious accounts.")
    print("Results saved to 'alerts' table in aml_system.db")

if __name__ == "__main__":
    run_anomaly_detection()