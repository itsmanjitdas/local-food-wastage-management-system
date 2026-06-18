import mysql.connector
import pandas as pd

# Connect to your local MySQL Server
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",                  # Default MySQL username
        password="Manjitdas1$" # CHANGE THIS to your actual MySQL workbench password!
    )
    cursor = db.cursor()
    print("Successfully connected to MySQL Server!")
    
    # Create the Database
    cursor.execute("CREATE DATABASE IF NOT EXISTS food_wastage_db;")
    cursor.execute("USE food_wastage_db;")
    print("Database 'food_wastage_db' initialized.")
    
    # Create Providers Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Providers (
        Provider_ID INT PRIMARY KEY,
        Name VARCHAR(255),
        Type VARCHAR(100),
        Address TEXT,
        City VARCHAR(100),
        Contact VARCHAR(50)
    );
    """)
    
    # Create Receivers Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Receivers (
        Receiver_ID INT PRIMARY KEY,
        Name VARCHAR(255),
        Type VARCHAR(100),
        City VARCHAR(100),
        Contact VARCHAR(50)
    );
    """)
    
    # Create Food Listings Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Food_Listings (
        Food_ID INT PRIMARY KEY,
        Food_Name VARCHAR(255),
        Quantity INT,
        Expiry_Date DATE,
        Provider_ID INT,
        Provider_Type VARCHAR(100),
        Location VARCHAR(100),
        Food_Type VARCHAR(100),
        Meal_Type VARCHAR(100),
        FOREIGN KEY (Provider_ID) REFERENCES Providers(Provider_ID)
    );
    """)

    # Create Claims Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Claims (
        Claim_ID INT PRIMARY KEY,
        Food_ID INT,
        Receiver_ID INT,
        Status VARCHAR(50),python database_setup.py
        Timestamp DATETIME,
        FOREIGN KEY (Food_ID) REFERENCES Food_Listings(Food_ID),
        FOREIGN KEY (Receiver_ID) REFERENCES Receivers(Receiver_ID)
    );
    """)
    
    db.commit()
    print("All database tables verified and created successfully!")

except mysql.connector.Error as err:
    print(f"Database Connection Error: {err}")
finally:
    if 'db' in locals() and db.is_connected():
        cursor.close()
        db.close()

