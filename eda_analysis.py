import mysql.connector
import pandas as pd

def run_exploratory_analysis():
    print("🚀 Initializing Programmatic EDA Operations Engine...")
    
    # Establish connection
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Manjitdas1$",
        database="food_wastage_db"
    )
    
    # 1. Quantity Summary Statistics via Pandas DataFrame Describe
    print("\n--- [A] Food Listing Quantity Descriptive Metrics ---")
    df_food = pd.read_sql("SELECT Quantity FROM Food_Listings", conn)
    print(df_food.describe())
    
    # 2. Category Counts Analysis
    print("\n--- [B] Claim Status Value Volumes ---")
    df_claims = pd.read_sql("SELECT Status FROM Claims", conn)
    print(df_claims.value_counts())
    
    # 3. Quick Dataset Shape Verification
    print("\n--- [C] Data Matrix Dimensional Verification ---")
    for table in ["Providers", "Receivers", "Food_Listings", "Claims"]:
        count = pd.read_sql(f"SELECT COUNT(*) as cnt FROM {table}", conn).iloc[0,0]
        print(f"✔ Table '{table}' Shape Matrix: Total Volume Registered = {count} Records.")

    conn.close()
    print("\n🏁 EDA Profile Complete.")

if __name__ == '__main__':
    run_exploratory_analysis()