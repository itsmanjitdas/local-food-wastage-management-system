import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px

# 1. Database Connection Helper Function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Manjitdas1$",  # Your active verified password
        database="food_wastage_db"
    )

# 2. Page Configuration
st.set_page_config(page_title="Local Food Wastage Management System", layout="wide")

# --- CUSTOM CSS FOR THE PREMIUM METRIC CARDS LOOK ---
st.markdown("""
    <style>
        div[data-testid="stMetricSimpleValue"] {
            font-size: 28px !important;
            font-weight: bold !important;
            color: #2E7D32 !important;
        }
        div[data-testid="stMetricLabel"] {
            font-size: 14px !important;
            color: #555555 !important;
        }
        .chart-header {
            background-color: #E8F5E9;
            padding: 10px;
            border-radius: 5px;
            font-weight: bold;
            color: #1B5E20;
            margin-bottom: 15px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("# 🥗 Local Food Wastage Management System")
st.markdown("### Connecting Surplus Food Providers to Those in Need")
st.write("---")

# 3. Sidebar Navigation Menu
st.sidebar.header("Navigation Panel")
menu_choice = st.sidebar.radio(
    "Go To:",
    ["📊 Insights & Trends (Analytics)", "🔍 Browse & Filter Listings", "⚙️ Administrative Operations (CRUD)"]
)

# -----------------------------------------------------------------------------
# TAB 1: INSIGHTS & TRENDS (Analytics & Aggregated Queries)
# -----------------------------------------------------------------------------
if menu_choice == "📊 Insights & Trends (Analytics)":
    st.header("📈 Food Wastage & Donation Analytics")
    st.write("Real-time metrics pulled via targeted SQL analysis queries.")
    
    # Open Connection safely inside the conditional block
    conn = get_db_connection()
    
    # --- KPI METRIC CARDS ROW ---
    total_providers = pd.read_sql("SELECT COUNT(*) FROM Providers", conn).iloc[0,0]
    total_receivers = pd.read_sql("SELECT COUNT(*) FROM Receivers", conn).iloc[0,0]
    total_listings = pd.read_sql("SELECT COUNT(*) FROM Food_Listings", conn).iloc[0,0]
    total_claims = pd.read_sql("SELECT COUNT(*) FROM Claims", conn).iloc[0,0]
    total_qty = pd.read_sql("SELECT SUM(Quantity) FROM Food_Listings", conn).iloc[0,0]
    completed_claims = pd.read_sql("SELECT COUNT(*) FROM Claims WHERE Status='Completed'", conn).iloc[0,0]

    # Display KPI rows side by side
    m1, m2, m3, m4, m5, m6 = st.columns(6)
    with m1:
        st.metric(label="🏪 Providers", value=f"{total_providers:,}")
    with m2:
        st.metric(label="🤝 Receivers", value=f"{total_receivers:,}")
    with m3:
        st.metric(label="📦 Listings", value=f"{total_listings:,}")
    with m4:
        st.metric(label="📝 Claims", value=f"{total_claims:,}")
    with m5:
        st.metric(label="🍖 Total Qty", value=f"{int(total_qty or 0):,}")
    with m6:
        st.metric(label="✅ Completed", value=f"{completed_claims:,}")
        
    st.write("---")

    # =========================================================================
    # 📊 CONDUCT BASIC EXPLORATORY DATA ANALYSIS (EDA)
    # =========================================================================
    with st.expander("📊 View Dataset Descriptive Statistics (EDA Summaries)"):
        st.write("**Food Listing Volumes (Quantity Distributions):**")
        df_desc = pd.read_sql("SELECT Quantity FROM Food_Listings", conn)
        st.dataframe(df_desc.describe().T, use_container_width=True)
        
        st.write("**Claims Status Value Counts:**")
        df_status_counts = pd.read_sql("SELECT Status, COUNT(*) as Total_Claims FROM Claims GROUP BY Status", conn)
        st.dataframe(df_status_counts, use_container_width=True, hide_index=True)
    
    st.write("---")

    # --- VISUALIZATION ROW 1: Providers and Receivers side by side ---
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown('<div class="chart-header">💡 Top Contributing Food Providers</div>', unsafe_allow_html=True)
        query_2 = """
        SELECT Provider_Type, SUM(Quantity) as Total_Food_Donated 
        FROM Food_Listings 
        GROUP BY Provider_Type 
        ORDER BY Total_Food_Donated DESC;
        """
        df_q2 = pd.read_sql(query_2, conn)
        
        fig2 = px.bar(df_q2, x="Provider_Type", y="Total_Food_Donated", 
                      labels={"Provider_Type": "Sector", "Total_Food_Donated": "Quantity (Units)"},
                      color="Total_Food_Donated", color_continuous_scale="Viridis")
        st.plotly_chart(fig2, use_container_width=True)
        
        with st.expander("View Raw Sector Contribution Data"):
            st.dataframe(df_q2, use_container_width=True, hide_index=True)
            
    with col_chart2:
        st.markdown('<div class="chart-header">📍 Providers and Receivers Breakdown by City</div>', unsafe_allow_html=True)
        query_1 = """
        SELECT City, 
               COUNT(DISTINCT Provider_ID) AS Total_Providers, 
               COUNT(DISTINCT Receiver_ID) AS Total_Receivers
        FROM (
            SELECT City, Provider_ID, NULL AS Receiver_ID FROM Providers
            UNION ALL
            SELECT City, NULL AS Provider_ID, Receiver_ID FROM Receivers
        ) as combined
        GROUP BY City;
        """
        df_q1 = pd.read_sql(query_1, conn)
        st.bar_chart(data=df_q1, x="City", y=["Total_Providers", "Total_Receivers"])
        st.dataframe(df_q1, use_container_width=True, hide_index=True)
        
    st.write("---")

    # --- VISUALIZATION ROW 2: Receivers and Claims Status side by side ---
    col_chart3, col_chart4 = st.columns(2)

    with col_chart3:
        st.markdown('<div class="chart-header">🏆 Top Food Receivers / Claimants</div>', unsafe_allow_html=True)
        query_4 = """
        SELECT r.Name, r.Type, COUNT(c.Claim_ID) as Total_Claims_Made
        FROM Receivers r
        JOIN Claims c ON r.Receiver_ID = c.Receiver_ID
        GROUP BY r.Receiver_ID, r.Name, r.Type
        ORDER BY Total_Claims_Made DESC
        LIMIT 5;
        """
        df_q4 = pd.read_sql(query_4, conn)
        fig4 = px.pie(df_q4, values="Total_Claims_Made", names="Name", title="Top 5 Organizations by Claims Volume")
        st.plotly_chart(fig4, use_container_width=True)
        
    with col_chart4:
        st.markdown('<div class="chart-header">📊 Claims Status Percentage Breakdown</div>', unsafe_allow_html=True)
        query_10 = """
        SELECT Status, 
               COUNT(*) as Total_Count,
               ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Claims), 2) as Percentage
        FROM Claims 
        GROUP BY Status;
        """
        df_q10 = pd.read_sql(query_10, conn)
        st.dataframe(df_q10, use_container_width=True, hide_index=True)

    # =========================================================================
    # 🗃️ COMPLETE 15 SQL QUERY INTEGRATION VAULT
    # =========================================================================
    st.write("---")
    st.header("🗃️ Complete Project SQL Query Vault (All 15 Queries)")
    st.write("Select a specific business question below to execute its corresponding SQL analysis live.")

    query_selection = st.selectbox(
        "Choose Analysis Question:",
        [
            "Select a query...",
            "Q1: Total food providers and receivers in each city",
            "Q2: Type of food provider that contributes the most food",
            "Q3: Contact information of food providers in Bangalore",
            "Q4: Receivers who have claimed the most food listings",
            "Q5: Total quantity of food available from all providers combined",
            "Q6: City with the highest number of food listings",
            "Q7: Most commonly available food types",
            "Q8: Number of food claims made for each food item",
            "Q9: Provider with the highest number of successful food claims",
            "Q10: Percentage breakdown of food claims status",
            "Q11: Average quantity of food claimed per receiver",
            "Q12: Meal type claimed the most (Breakfast, Lunch, Dinner, Snacks)",
            "Q13: Total quantity of food donated by each provider",
            "Q14: Food listings that expired before being claimed",
            "Q15: Monthly trend of food claims made"
        ]
    )

    if query_selection != "Select a query...":
        sql_map = {
            "Q1: Total food providers and receivers in each city":
                "SELECT City, COUNT(DISTINCT Provider_ID) AS Total_Providers, COUNT(DISTINCT Receiver_ID) AS Total_Receivers FROM (SELECT City, Provider_ID, NULL AS Receiver_ID FROM Providers UNION ALL SELECT City, NULL AS Provider_ID, Receiver_ID FROM Receivers) as Combined GROUP BY City;",
            
            "Q2: Type of food provider that contributes the most food":
                "SELECT Provider_Type, SUM(Quantity) AS Total_Food_Donated FROM Food_Listings GROUP BY Provider_Type ORDER BY Total_Food_Donated DESC;",
                
            "Q3: Contact information of food providers in Bangalore": 
                "SELECT Name, Type, Contact, Address, City FROM Providers WHERE City = 'Bangalore';",
                
            "Q4: Receivers who have claimed the most food listings":
                "SELECT r.Name, r.Type, COUNT(c.Claim_ID) AS Total_Claims FROM Receivers r JOIN Claims c ON r.Receiver_ID = c.Receiver_ID GROUP BY r.Receiver_ID, r.Name, r.Type ORDER BY Total_Claims DESC;",

            "Q5: Total quantity of food available from all providers combined": 
                "SELECT SUM(Quantity) AS Total_Available_Food FROM Food_Listings;",
                
            "Q6: City with the highest number of food listings": 
                "SELECT Location AS City, COUNT(Food_ID) AS Total_Listings FROM Food_Listings GROUP BY Location ORDER BY Total_Listings DESC LIMIT 1;",
                
            "Q7: Most commonly available food types": 
                "SELECT Food_Type, COUNT(*) AS Listing_Count, SUM(Quantity) AS Total_Quantity FROM Food_Listings GROUP BY Food_Type ORDER BY Total_Quantity DESC;",
                
            "Q8: Number of food claims made for each food item": 
                "SELECT fl.Food_Name, COUNT(c.Claim_ID) AS Total_Claims_Made FROM Food_Listings fl LEFT JOIN Claims c ON fl.Food_ID = c.Food_ID GROUP BY fl.Food_Name ORDER BY Total_Claims_Made DESC;",
                
            "Q9: Provider with the highest number of successful food claims": 
                "SELECT p.Name, COUNT(c.Claim_ID) AS Successful_Claims FROM Providers p JOIN Food_Listings fl ON p.Provider_ID = fl.Provider_ID JOIN Claims c ON fl.Food_ID = c.Food_ID WHERE c.Status = 'Completed' GROUP BY p.Provider_ID, p.Name ORDER BY Successful_Claims DESC LIMIT 1;",
                
            "Q10: Percentage breakdown of food claims status":
                "SELECT Status, COUNT(*) AS Count, ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Claims), 2) AS Percentage FROM Claims GROUP BY Status;",

            "Q11: Average quantity of food claimed per receiver": 
                "SELECT r.Name, ROUND(AVG(fl.Quantity), 2) AS Avg_Quantity_Claimed FROM Receivers r JOIN Claims c ON r.Receiver_ID = c.Receiver_ID JOIN Food_Listings fl ON c.Food_ID = fl.Food_ID GROUP BY r.Receiver_ID, r.Name;",
                
            "Q12: Meal type claimed the most (Breakfast, Lunch, Dinner, Snacks)": 
                "SELECT fl.Meal_Type, COUNT(c.Claim_ID) AS Claims_Count FROM Food_Listings fl JOIN Claims c ON fl.Food_ID = c.Food_ID GROUP BY fl.Meal_Type ORDER BY Claims_Count DESC;",
                
            "Q13: Total quantity of food donated by each provider": 
                "SELECT p.Name, p.Type, SUM(fl.Quantity) AS Total_Donated FROM Providers p JOIN Food_Listings fl ON p.Provider_ID = fl.Provider_ID GROUP BY p.Provider_ID, p.Name, p.Type ORDER BY Total_Donated DESC;",
                
            "Q14: Food listings that expired before being claimed": 
                "SELECT fl.Food_Name, fl.Expiry_Date, fl.Location FROM Food_Listings fl LEFT JOIN Claims c ON fl.Food_ID = c.Food_ID WHERE fl.Expiry_Date < CURDATE() AND (c.Claim_ID IS NULL OR c.Status = 'Cancelled');",
                
            "Q15: Monthly trend of food claims made": 
                "SELECT DATE_FORMAT(Timestamp, '%Y-%m') AS Month, COUNT(Claim_ID) AS Total_Claims FROM Claims GROUP BY Month ORDER BY Month ASC;"
        }
        
        target_sql = sql_map[query_selection]
        df_result = pd.read_sql(target_sql, conn)
        
        st.markdown(f"**Executing Query Link Schema:**")
        st.code(target_sql, language="sql")
        st.dataframe(df_result, use_container_width=True, hide_index=True)

    conn.close()

# -----------------------------------------------------------------------------
# TAB 2: BROWSE & FILTER LISTINGS
# -----------------------------------------------------------------------------
elif menu_choice == "🔍 Browse & Filter Listings":
    st.header("📋 Live Food Marketplace")
    st.write("Filter active surplus listings to claim items before expiration.")
    
    conn = get_db_connection()
    df_listings = pd.read_sql("SELECT * FROM Food_Listings", conn)
    conn.close()
    
    # Dynamic Filter UI Columns
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_city = st.multiselect("Filter by City Location:", options=df_listings["Location"].dropna().unique())
    with col2:
        selected_food_type = st.multiselect("Filter by Food Category:", options=df_listings["Food_Type"].dropna().unique())
    with col3:
        selected_meal = st.multiselect("Filter by Meal Type:", options=df_listings["Meal_Type"].dropna().unique())
        
    # Apply user filtering choices
    if selected_city:
        df_listings = df_listings[df_listings["Location"].isin(selected_city)]
    if selected_food_type:
        df_listings = df_listings[df_listings["Food_Type"].isin(selected_food_type)]
    if selected_meal:
        df_listings = df_listings[df_listings["Meal_Type"].isin(selected_meal)]
        
    st.dataframe(df_listings, use_container_width=True, hide_index=True)

# -----------------------------------------------------------------------------
# TAB 3: CRUD OPERATIONS (Create, Read, Update, Delete)
# -----------------------------------------------------------------------------
elif menu_choice == "⚙️ Administrative Operations (CRUD)":
    st.header("🔧 Database CRUD Operations Interface")
    
    action = st.selectbox("Database Action:", ["Add New Surplus Record (CREATE)", "Update Claim Status (UPDATE)", "Remove Food Listing (DELETE)"])
    
    # 1. CREATE OPERATION
    if action == "Add New Surplus Record (CREATE)":
        st.subheader("➕ List New Surplus Item Into System")
        with st.form("insert_form", clear_on_submit=True):
            f_id = st.number_input("Food Item ID (Unique Integer)", step=1)
            f_name = st.text_input("Food Item Name (e.g., Cooked Rice, Salads)")
            f_qty = st.number_input("Total Quantity (Units)", min_value=1, step=1)
            f_date = st.date_input("Item Expiry Date")
            f_prov_id = st.number_input("Provider Business ID Reference", step=1)
            
            submit_btn = st.form_submit_button("Publish Listing")
            
            if submit_btn:
                conn = get_db_connection()
                cursor = conn.cursor()
                try:
                    cursor.execute(
                        "INSERT INTO Food_Listings (Food_ID, Food_Name, Quantity, Expiry_Date, Provider_ID) VALUES (%s, %s, %s, %s, %s)",
                        (f_id, f_name, f_qty, f_date, f_prov_id)
                    )
                    conn.commit()
                    st.success(f"🎉 Success! Added record '{f_name}' to system inventory.")
                except mysql.connector.Error as err:
                    st.error(f"Database insertion failed: {err}")
                finally:
                    conn.close()

    # 2. UPDATE OPERATION
    elif action == "Update Claim Status (UPDATE)":
        st.subheader("🔄 Update Active Claim Tracker Status")
        with st.form("update_form"):
            claim_id_to_up = st.number_input("Enter target Claim ID to modify:", step=1)
            new_status = st.selectbox("Select New Status Assignment:", ["Pending", "Completed", "Cancelled"])
            update_btn = st.form_submit_button("Commit Status Update")
            
            if update_btn:
                conn = get_db_connection()
                cursor = conn.cursor()
                try:
                    cursor.execute("UPDATE Claims SET Status = %s WHERE Claim_ID = %s", (new_status, claim_id_to_up))
                    conn.commit()
                    st.success(f"✏️ Claim ID {claim_id_to_up} has been updated to '{new_status}' successfully.")
                except mysql.connector.Error as err:
                    st.error(f"Database update failed: {err}")
                finally:
                    conn.close()

    # 3. DELETE OPERATION
    elif action == "Remove Food Listing (DELETE)":
        st.subheader("🗑️ Remove Food Item Record From Registry")
        with st.form("delete_form"):
            food_id_to_del = st.number_input("Enter exact Food ID to permanently erase:", step=1)
            delete_btn = st.form_submit_button("Confirm Permanent Deletion")
            
            if delete_btn:
                conn = get_db_connection()
                cursor = conn.cursor()
                try:
                    cursor.execute("DELETE FROM Food_Listings WHERE Food_ID = %s", (food_id_to_del,))
                    conn.commit()
                    st.warning(f"⚠️ Food Item ID {food_id_to_del} has been cleanly purged from database tables.")
                except mysql.connector.Error as err:
                    st.error(f"Database deletion failed: {err}")
                finally:
                    conn.close()