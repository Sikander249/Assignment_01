import streamlit as st
import pandas as pd
import sqlite3

# --Database connection --
def get_db_connection():
    conn = sqlite3.connect('bank.db')
    return conn

def apply_futuristic_styling():
    st.markdown("""
        <style>
        /* Make header and menu invisible by default, but appear on hover */
        header {
            opacity: 0 !important;
            transition: opacity 0.3s ease-in-out !important;
        }
        header:hover {
            opacity: 1 !important;
        }
                
        /* keep the sidebar always visible with a slight transparency */
        [data-testid="stSidebar"] {
            position: fixed;
            top: 0;
            left: 0;
            height: 100vh;
            width: 250px;
            background-color: rgba(40, 44, 52, 0.9) !important; /* Semi-transparent dark background */
            z-index: 1000;
        }
        /* keep the footer permanent hidden to keep it clean */
            footer {visibility: hidden;}
                    
        /* Add a glowing neon effect to all main titles*/
        h1 {
            color: #00e5ff !important;
            text-shadow: 05px 05px 20px rgba(0, 229, 255, 0.6);
            font-family: 'Courier New', Courier, monospace;
        }
        h2, h3 {
            color: #bd93f9 !important; /* Neon purple for subheadings */
        }
        /* Glassmorphism effect for the sidebar */
        [data-testid="stSidebar"] {
            border-right: 1px solid rgba(0, 229, 255, 0.2);
        }
        /* Style the dataframes tables to look like data terminals */
        .stDataFrame {
            border: 1px solid #00e5ff;
            border-radius: 5px;
            box-shadow: 0px 0px 10px rgba(0, 229, 255, 0.2);
        }
        </style>
    """, unsafe_allow_html=True)

# --App confirguration ---
st.set_page_config(page_title="BankSight Dashboard", page_icon="🏦", layout="wide")
apply_futuristic_styling()

# --Sidebar Navigation ---
st.sidebar.title("🏦 BankSight Navigation")
pages = st.sidebar.radio("Go to", [
    "🏠 Introduction", 
    "📊 View Tables", 
    "🔍 Filter Data", 
    "✏️ CRUD Operations", 
    "💰 Credit / Debit Simulation", 
    "🧠 Analytical Insights", 
    "👩‍💻 About Creator"
])

# --pages---

if pages == "🏠 Introduction":
    st.title("⚡ BankSight: Command Center")
    st.markdown("### System Status: ONLINE | Anomaly Detection: ACTIVE")

    st.markdown("---")

   # Connect to DB and get real numbers for our dashboard
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM customers")
    total_cust = cursor.fetchone()[0]
   
    cursor.execute("SELECT COUNT(*) FROM transactions")
    total_txn = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(account_balance) FROM accounts")
    total_assets = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM transactions WHERE status = 'failed' OR txn_type='online fraud'")
    total_alerts = cursor.fetchone()[0]

    conn.close()
    #Layoput metrics in 4 neat columns
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(label="👥Total Customers", value=f"{total_cust:,}")
    with col2:
        st.metric(label="💳 Total Transactions", value=f"{total_txn:,}")
    with col3:
        st.metric(label="💰 Total Assets (₹)", value=f"{total_assets:,.0f}")
    with col4:
        st.metric(label="🚨 Active Alerts", value=f"{total_alerts:,}", delta="-2% (Normal)", delta_color="inverse")
    
    st.markdown("---")

# LAYOUT TWO COLUMNS FOR TEXT INFO
    info_col1, info_col2 = st.columns(2)
    with info_col1:
        st.info("**Primary Objective:** Real-time transaction monitoring, demographic profiling, and high-risk anomaly detection.")
    with info_col2:
        st.warning("**Security Protocol:** CRUD operations on live accounts are heavily monitored. Ensure minimum balances are maintained")
  
elif pages == "📊 View Tables":
    st.title("📊 View Raw Database Tables")
    table_name = st.selectbox("Select Table to View", ["customers", "accounts", "transactions", "branches", "loans", "credit_cards", "support_tickets"])
    conn = get_db_connection()
    df = pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT 600", conn)
    st.dataframe(df)
    conn.close()

elif pages == "🔍 Filter Data":
    st.title("🔍 Multi-level Data Filtering")
    table = st.selectbox("Select Database", ["customers", "transactions", "accounts", "loans", "branches", "support_tickets", "credit_cards"])
    conn = get_db_connection()

    if table == "customers":
        st.subheader("Filter Customers Data")

# Organise filters into columns for a clean UI
        col1, col2, col3 = st.columns(3)
        
        with col1:
            c_id = st.text_input("Customer ID (e.g., C0001)")
            c_name = st.text_input("Customer Name")

        with col2:
            age_range = st.slider("Age Range", 18, 80, (18, 80))
            city = st.text_input("City")

        with col3:
            account_type = st.selectbox("Account Type", ["All", "Savings", "Current"])
            gender = st.selectbox("Gender", ["All", "M", "F"])

#date_range picker for join_date
        join_date_range = st.date_input("Join Date Range", value=None, min_value=None, max_value=None)

#Base query
        query = "SELECT * FROM customers WHERE 1=1"
        params = []

#partial or exact matchs
        if c_id:
            query += " AND customer_id LIKE ?"
            params.append(f"%{c_id}%")
        if c_name:
            query += " AND name LIKE ?"
            params.append(f"%{c_name}%")
        if city:
            query += " AND city LIKE ?"
            params.append(f"%{city}%")
        if age_range:
            query += " AND age BETWEEN ? AND ?"
            params.extend([age_range[0], age_range[1]])
        if account_type != "All":
            query += " AND account_type = ?"
            params.append(account_type)
        if gender != "All":
            query += " AND gender = ?"
            params.append(gender)
        if join_date_range is not None and len(join_date_range) == 2:
            query += " AND join_date BETWEEN ? AND ?"
            params.extend([str(join_date_range[0], str(join_date_range[1]))])

# Execute query with parameters
        df = pd.read_sql_query(query, conn, params=params)
        st.write(f"**Results Found:** {len(df)}")
        st.dataframe(df)

    elif table == "transactions":
        txn_type = st.selectbox("Filter by Txn Type", ["All", "deposit", "withdrawal", "transfer", "purchase", "online"])
        status = st.selectbox("Filter by Status", ["All", "success", "failed", "pending"])

        query = "SELECT * FROM transactions WHERE 1=1"
        if txn_type != "All":
            query += f" AND txn_type = '{txn_type}'"
        if status != "All":
            query += f" AND status = '{status}'"

        df = pd.read_sql_query(query, conn)
        st.dataframe(df)

    elif table == "accounts":
        st.subheader("Filter Accounts Data")
        col1, col2 = st.columns(2)

        with col1:
            c_id = st.text_input("Customer ID (e.g., C0001)")
        with col2:
            min_balance = st.number_input("Minimum Balance", min_value=0, value=0)

        query = "SELECT * FROM accounts WHERE 1=1"
        params = []
    
        if c_id:
            query += " AND customer_id LIKE ?"
            params.append(f"%{c_id}%")
        if min_balance > 0:
            query += " AND account_balance >= ?"
            params.append(min_balance)
    
        df = pd.read_sql_query(query, conn, params=params)
        st.write(f"**Results Found:** {len(df)}")
        st.dataframe(df)
    
    elif table == "loans":
        st.subheader("Filter Loans Data")
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            loan_type = st.selectbox("Loan Type", ["All", "Home", "Personal", "Auto", "Education"])
        with col2:
            loan_status = st.selectbox("Loan Status", ["All", "Active", "Closed", "Defaulted", "Approved"])
        with col3:
            min_amount = st.number_input("Minimum Loan Amount", min_value=0, value=0)
        with col4:
            cx_id = st.text_input("Customer ID (e.g., 0001)")
        with col5:
            acc_id = st.text_input("Account ID (e.g., 0001)")
        query = "SELECT * FROM loans WHERE 1=1"
        params = []

        if loan_type != "All":
            query += " AND Loan_Type = ?"
            params.append(loan_type)
        if loan_status != "All":
            query += " AND Loan_Status = ?"
            params.append(loan_status)
        if min_amount > 0:
            query += " AND Loan_Amount >= ?"
            params.append(min_amount)
        if cx_id:
            query += " AND Customer_ID LIKE ?"
            params.append(f"%{cx_id}%")
        if acc_id:
            query += " AND Account_ID LIKE ?"
            params.append(f"%{acc_id}%")
        df = pd.read_sql_query(query, conn, params=params)
        st.write(f"**Results Found:** {len(df)}")
        st.dataframe(df)

    elif table == "branches":
        st.subheader("Filter Branches Data")
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            branch_name = st.text_input("Branch Name")
        with col2:
            city = st.text_input("City")
        with col3:
            Manager_name = st.text_input("Manager Name")
        with col4:
            Total_employees = st.number_input("Minimum Employees", min_value=0, value=0)
        with col5:
            Performance_Rating = st.selectbox("Performance_Rating", ["ALL", 1, 2, 3, 4, 5])

        query = "SELECT * FROM branches WHERE 1=1"
        params = []

        if branch_name:
            query += " AND Branch_Name LIKE ?"
            params.append(f"%{branch_name}%")
        if city:
            query += " AND City LIKE ?"
            params.append(f"%{city}%")
        if Manager_name:
            query += " AND Manager_Name LIKE ?"
            params.append(f"%{Manager_name}%")
        if Total_employees > 0:
            query += " AND Total_Employees >= ?"
            params.append(Total_employees)
        if Performance_Rating != "ALL":
            query += " AND Performance_Rating = ?"
            params.append(Performance_Rating)

        df = pd.read_sql_query(query, conn, params=params)
        st.write(f"**Results Found:** {len(df)}")
        st.dataframe(df)

    elif table == "support_tickets":
        st.subheader("Filter Support Tickets Data")
        col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns(9)

        with col1:
            ticket_id = st.text_input("Ticket ID (e.g., T00001)")
        with col2:
            customer_id = st.text_input("Customer ID (e.g., C0001)")
        with col3:
            acc_id = st.text_input("Account ID (e.g., A0001)")
        with col4:
            branch_name = st.text_input("Branch Name")
        with col5:
            Priority = st.selectbox("Priority", ["All", "Low", "Medium", "High", "Critical"])
        with col6:
            status = st.selectbox("Status", ["All", "Open", "In Progress", "Resolved", "Closed"])
        with col7:
            Agent = st.text_input("Support_Agent Name")
        with col8:
            Channel = st.selectbox("Channel", ["All", "Mobile App", "Email", "Phone", "In-Person"])
        with col9:
            rating = st.selectbox("Customer_Rating", ["ALL", 0, 1, 2, 3, 4, 5])

        query = "SELECT * FROM support_tickets WHERE 1=1"
        params = []

        if ticket_id:
            query += " AND Ticket_ID LIKE ?"
            params.append(f"%{ticket_id}%")
        if customer_id:
            query += " AND Customer_ID LIKE ?"
            params.append(f"%{customer_id}%")
        if acc_id:
            query += " AND Account_ID LIKE ?"
            params.append(f"%{acc_id}%")
        if branch_name:
            query += " AND Branch LIKE ?"
            params.append(f"%{branch_name}%")
        if Priority != "All":
            query += " AND Priority = ?"
            params.append(Priority)
        if status != "All":
            query += " AND Status = ?"
            params.append(status)
        if Agent:
            query += " AND Support_Agent LIKE ?"
            params.append(f"%{Agent}%")
        if Channel != "All":
            query += " AND Channel = ?"
            params.append(Channel)
        if rating != "ALL":
            query += " AND Customer_Rating = ?"
            params.append(rating)

        df = pd.read_sql_query(query, conn, params=params)
        st.write(f"**Results Found:** {len(df)}")
        st.dataframe(df)

    elif table == "credit_cards":
        st.subheader("Filter Credit Cards Data")
        col1, col2, col3, col4, col5, col6 = st.columns(6)

        with col1:
            cx_id = st.text_input("Customer ID (e.g., 0001)")
        with col2:
            acc_id = st.text_input("Account ID (e.g., 0001)")
        with col3:
            card_Number = st.text_input("Card Number (e.g., 0000000000000001)")
        with col4:
            card_type = st.selectbox("Card Type", ["All", "Silver", "Gold", "Platinum", "Business"])
        with col5:
            card_Network = st.selectbox("Card Network", ["All", "Visa", "MasterCard", "Amex", "Discover"])
        with col6:
            Status = st.selectbox("Status", ["All", "Active", "Blocked", "Expired"])

        query = "SELECT * FROM credit_cards WHERE 1=1"
        params = []

        if cx_id:
            query += " AND Customer_ID LIKE ?"
            params.append(f"%{cx_id}%")
        if acc_id:
            query += " AND Account_ID LIKE ?"
            params.append(f"%{acc_id}%")
        if card_Number:
            query += " AND Card_Number LIKE ?"
            params.append(f"%{card_Number}%")
        if card_type != "All":
            query += " AND Card_Type = ?"
            params.append(card_type)
        if card_Network != "All":
            query += " AND Card_Network = ?"
            params.append(card_Network)
        if Status != "All":
            query += " AND Status = ?"
            params.append(Status)
        
        df = pd.read_sql_query(query, conn, params=params)
        st.write(f"**Results Found:** {len(df)}")
        st.dataframe(df)
    conn.close()
        
elif pages == "✏️ CRUD Operations":
    st.title("✏️ Manage Customers (CRUD)")
    conn = get_db_connection()
    cursor = conn.cursor()

    operation = st.radio("Operation", ["Create", "Update", "Delete"])

    if operation == "Create":
        c_id = st.text_input("Customer ID")
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=18)
        city = st.text_input("City")
        if st.button("Add Customer"):
            cursor.execute("INSERT INTO customers (customer_id, name, age, city) VALUES (?, ?, ?, ?)", (c_id, name, age, city))
            conn.commit()
            st.success("Customer added successfully!")

    elif operation == "Update":
        c_id = st.text_input("Customer ID to Update")
        new_city = st.text_input("New City")
        if st.button("Update Customer"):
            cursor.execute("UPDATE customers SET city = ? WHERE customer_id = ?", (new_city, c_id))
            conn.commit()
            st.success("Customer updated successfully!")

    elif operation == "Delete":
        c_id = st.text_input("Customer ID to Delete")
        if st.button("Delete Customer"):
            cursor.execute("DELETE FROM customers WHERE customer_id = ?", (c_id,))
            conn.commit()
            st.success("Customer deleted successfully!")
    conn.close()

elif pages == "💰 Credit / Debit Simulation":
    st.title("💰 Transaction Simulation")
    conn = get_db_connection()
    cursor = conn.cursor()

    c_id = st.text_input("Enter Customer ID (e.g., C0001)")
    if c_id:
        cursor.execute("SELECT account_balance FROM customers WHERE customer_id = ?", (c_id,))
        res = cursor.fetchone()
        if res:
            balance = res[0]
            st.info(f"Current Balance: ₹{balance:.2f}")

            amount = st.number_input("Enter Amount", min_value=1.0)
            op = st.radio("Operation", ["Deposit", "Withdraw"])

            if st.button("Execute Transaction"):
                if op == "Withdraw" and (balance - amount < 1000):
                    st.error("Transaction Failed! Minimum balance of ₹1000 must be maintained.")
                else:
                    new_bal = balance + amount if op == "Deposit" else balance - amount
                    cursor.execute("UPDATE customers SET account_balance = ? WHERE customer_id = ?", (new_bal, c_id))
                    conn.commit()
                    st.success(f"Transaction successful! New Balance: ₹{new_bal:.2f}")
        else:
            st.error("Customer Account not found.")
    conn.close()

elif pages == "🧠 Analytical Insights":
    st.title("🧠 Analytical SQL Insights")

    queries = {
        "Q1: Customers per city & average balance": """
            SELECT c.city, COUNT(c.customer_id) as total_customers, ROUND(AVG(a.account_balance), 2) as avg_balance
            FROM customers c JOIN accounts a ON c.customer_id = a.customer_id
            GROUP BY c.city ORDER BY total_customers DESC;
            """,
        "Q2: Account type with highest total balance": """
            SELECT c.account_type, SUM(a.account_balance) as total_balance 
            FROM customers c JOIN accounts a ON c.customer_id = a.customer_id 
            GROUP BY c.account_type ORDER BY total_balance DESC LIMIT 1;
        """,
        "Q3: Top 10 customers by total balance": """
            SELECT c.name, a.account_balance 
            FROM customers c JOIN accounts a ON c.customer_id = a.customer_id 
            ORDER BY a.account_balance DESC LIMIT 10;
        """,
        "Q4: Customers who opened accounts in 2023 with balance > ₹1,00,000": """
            SELECT c.name, a.account_balance, c.join_date 
            FROM customers c JOIN accounts a ON c.customer_id = a.customer_id 
            WHERE strftime('%Y', c.join_date) = '2023' AND a.account_balance > 100000;
        """,
        "Q5: Total transaction volume by transaction type": """
            SELECT txn_type, SUM(amount) as total_volume FROM transactions GROUP BY txn_type;
        """,
        "Q6: Failed transactions per transaction type": """
            SELECT txn_type, COUNT(*) as failed_count FROM transactions WHERE status = 'failed' GROUP BY txn_type;
        """,
        "Q7: Total number of transactions per transaction type": """
            SELECT txn_type, COUNT(*) as total_count FROM transactions GROUP BY txn_type;
        """,
        "Q8: Accounts with 5+ high-value transactions (>₹20,000)": """
            SELECT customer_id, COUNT(*) as high_value_txns 
            FROM transactions WHERE amount > 20000 GROUP BY customer_id HAVING COUNT(*) >= 5;
        """,
        "Q9: Average loan amount and interest rate by loan type": """
            SELECT Loan_Type, ROUND(AVG(Loan_Amount),2) as avg_amount, ROUND(AVG(Interest_Rate),2) as avg_interest 
            FROM loans GROUP BY Loan_Type;
        """,
        "Q10: Customers with more than one active/approved loan": """
            SELECT Customer_ID, COUNT(*) as total_active_loans 
            FROM loans WHERE Loan_Status IN ('Active', 'Approved') GROUP BY Customer_ID HAVING COUNT(*) > 1;
        """,
        "Q11: Top 5 customers with highest outstanding loan amounts": """
            SELECT Customer_ID, SUM(Loan_Amount) as outstanding_amount 
            FROM loans WHERE Loan_Status != 'Closed' GROUP BY Customer_ID ORDER BY outstanding_amount DESC LIMIT 5;
        """,
        "Q12: Average loan amount per branch": """
            SELECT Branch, ROUND(AVG(Loan_Amount),2) as avg_loan_amount FROM loans GROUP BY Branch;
        """,
        "Q13: Customers in each age group": """
            SELECT 
                CASE 
                    WHEN age BETWEEN 18 AND 25 THEN '18-25'
                    WHEN age BETWEEN 26 AND 35 THEN '26-35'
                    WHEN age BETWEEN 36 AND 50 THEN '36-50'
                    ELSE '50+' 
                END as age_group, COUNT(*) as count 
            FROM customers GROUP BY age_group ORDER BY age_group;
        """,
        "Q14: Issue categories with longest avg resolution time (Days)": """
            SELECT Issue_Category, ROUND(AVG(julianday(Date_Closed) - julianday(Date_Opened)), 2) AS avg_resolution_days 
            FROM support_tickets WHERE Date_Closed IS NOT NULL 
            GROUP BY Issue_Category ORDER BY avg_resolution_days DESC;
        """,
        "Q15: Support agents with most critical tickets & high ratings (>=4)": """
            SELECT Support_Agent, COUNT(*) as high_rated_critical_resolutions 
            FROM support_tickets 
            WHERE Priority = 'Critical' AND Status IN ('Resolved', 'Closed') AND Customer_Rating >= 4 
            GROUP BY Support_Agent ORDER BY high_rated_critical_resolutions DESC;
        """
    }

    selected_q = st.selectbox("Select a query to execute", list(queries.keys()))
    sql_code = queries[selected_q]

    st.code(sql_code, language="sql")

    if st.button("Run Query"):
        conn = get_db_connection()
        df = pd.read_sql_query(sql_code, conn)
        st.dataframe(df)
        conn.close()

elif pages == "👩‍💻 About Creator":
    st.title("👩‍💻 About the Creator")
    st.markdown("""
    **Name:** Sikander Azhar Zaidi
                
    **Background:** Data Analyst with a passion for turning complex data into actionable insights.
                
    **Expertise:** Python, SQL, Streamlit, Data Analytics.
                
    **GitHub:** [Your GitHub URL]
                
    *Developed for the BankSight Intelligence Dashboard Project.*
    """)