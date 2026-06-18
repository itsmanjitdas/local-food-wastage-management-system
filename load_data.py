import mysql.connector
import pandas as pd

try:
    # Connect to the specific database we just created
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Manjitdas1$", # Use your actual MySQL password here too!
        database="food_wastage_db"
    )
    cursor = db.cursor()
    print("Connected to food_wastage_db successfully!")

    # --- 1. LOAD PROVIDERS DATA ---
    print("Loading Providers data...")
    providers_df = pd.read_csv("providers_data.csv")
    for _, row in providers_df.iterrows():
        sql = """INSERT INTO Providers (Provider_ID, Name, Type, Address, City, Contact) 
                 VALUES (%s, %s, %s, %s, %s, %s) 
                 ON DUPLICATE KEY UPDATE Name=VALUES(Name);"""
        cursor.execute(sql, tuple(row))
    
    # --- 2. LOAD RECEIVERS DATA ---
    print("Loading Receivers data...")
    receivers_df = pd.read_csv("receivers_data.csv")
    for _, row in receivers_df.iterrows():
        sql = """INSERT INTO Receivers (Receiver_ID, Name, Type, City, Contact) 
                 VALUES (%s, %s, %s, %s, %s) 
                 ON DUPLICATE KEY UPDATE Name=VALUES(Name);"""
        cursor.execute(sql, tuple(row))

   # --- 3. LOAD FOOD LISTINGS DATA ---
    print("Loading Food Listings data...")
    food_df = pd.read_csv("food_listings_data.csv")
    
    # FIX: Convert Expiry_Date column to correct YYYY-MM-DD format for SQL
    food_df['Expiry_Date'] = pd.to_datetime(food_df['Expiry_Date']).dt.strftime('%Y-%m-%d')
    
    for _, row in food_df.iterrows():
        sql = """INSERT INTO Food_Listings (Food_ID, Food_Name, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location, Food_Type, Meal_Type) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) 
                 ON DUPLICATE KEY UPDATE Food_Name=VALUES(Food_Name);"""
        cursor.execute(sql, tuple(row))

    # --- 4. LOAD CLAIMS DATA ---
    print("Loading Claims data...")
    claims_df = pd.read_csv("claims_data.csv")
    
    # FIX: Convert Timestamp column to correct YYYY-MM-DD HH:MM:SS format for SQL
    claims_df['Timestamp'] = pd.to_datetime(claims_df['Timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
    
    for _, row in claims_df.iterrows():
        sql = """INSERT INTO Claims (Claim_ID, Food_ID, Receiver_ID, Status, Timestamp) 
                 VALUES (%s, %s, %s, %s, %s) 
                 ON DUPLICATE KEY UPDATE Status=VALUES(Status);"""
        cursor.execute(sql, tuple(row))

    db.commit()
    print("🎉 All 4 CSV datasets have been successfully loaded into MySQL tables!")

except mysql.connector.Error as err:
    print(f"Error while loading data: {err}")
except FileNotFoundError as e:
    print(f"File missing error: {e}. Please make sure your CSVs are in the folder!")
finally:
    if 'db' in locals() and db.is_connected():
        cursor.close()
        db.close()