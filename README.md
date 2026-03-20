# Assignment_01
BankSight: Transaction Intelligence Dashboard

🏦 BankSight: Transaction Intelligence Dashboard

📌 Project Overview

BankSight is a comprehensive Banking Transaction Insights system built to process, analyze, and visualize daily banking operations. Banks process millions of transactions daily, and this project provides a solution to understand customer behavior, identify transaction trends, evaluate branch performance, and detect potentially fraudulent activity early.

![Capture](https://github.com/user-attachments/assets/d270c784-c857-4c33-85ac-07d2e585bb97)

![Capture 02](https://github.com/user-attachments/assets/f58bb936-9292-4094-bbb1-f0a59f711f11)

![Capture 03](https://github.com/user-attachments/assets/a8357c2d-59ee-4e82-89e8-4d641ec44c69)


Domain: Banking, Finance, Customer Behavior Analysis, Fraud Prevention

🎯 Business Use Cases
Customer Profiling: Tailoring banking products based on demographic and transaction behavior.

Fraud Prevention: Identifying high-risk transactions and accounts.

Performance Evaluation: Assessing branch performance based on loan issuance and support ticket resolution.

Interactive Querying: Enabling bank officials to seamlessly explore databases and simulate live transactions.

🚀 Features & Application Modules
The interactive Streamlit application contains the following core modules:

🏠 Command Center: Real-time KPI metrics showing total customers, transactions, assets, and security alerts.

📊 View Tables: Direct access to view the raw data from the 7 core datasets.

🔍 Multi-level Filtering: Advanced filtering capabilities across all datasets using safe, parameterized SQL queries.

✏️ CRUD Operations: Full capability to Create, Read, Update, and Delete customer records directly into the SQLite database.

💰 Credit / Debit Simulation: A live transaction simulator that enforces a minimum balance rule (₹1000) and securely updates the database.

🧠 Analytical Insights: Execution of 15+ complex real-world SQL queries (covering aggregations, joins, filtering, and date manipulations).

🗄️ Data Architecture & Datasets
The project utilizes a local SQLite database (banksight.db) integrating both .csv and .json files.

Customers: Demographics, age, and account types.

Accounts: Account balances and last updated timestamps.

Transactions: Detailed logs of deposits, withdrawals, transfers, and online fraud.

Loans: Loan types, interest rates, and operational status.

Credit Cards: Card tiers, networks, credit limits, and expiry dates.

Branches: Location, manager details, and performance ratings.

Support Tickets: Customer service interactions, issue categories, and resolution times.

🛠️ Tech Stack
Language: Python

Database: SQL (SQLite3)

Frontend/Dashboard: Streamlit

Data Manipulation: Pandas

💻 Installation & Local Setup
To run this project locally on your machine, follow these steps:

1. Install required dependencies:
(Ensure you have Python installed, then install Pandas and Streamlit)

pip install pandas streamlit
2. Run the Database Setup Script:
(This will read the raw CSV/JSON files and generate the bank.db SQLite database)

python setup_db.py
3. Launch the Streamlit App:

streamlit run app.py
📊 Analytical SQL Insights Covered
This project demonstrates proficiency in SQL by answering 15 complex business questions, including:

Calculating transaction volume by type.

Identifying accounts with 5+ high-value transactions (>₹20,000) for fraud detection.

Finding the top 10 customers by total account balance.

Calculating the average resolution time for customer support tickets by issue category.

Evaluating the average loan amount issued per branch.

(All SQL queries can be viewed and executed interactively within the app's "Analytical Insights" page).

👨‍💻 About the Creator
[Sikander Azhar Zaidi]

Role: Data Analyst

Expertise: Python, SQL, Streamlit, Data Analytics
