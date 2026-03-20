import pandas as pd
import sqlite3
import os
import json

def create_database():
    # connect to SQLite database (creates it if it doesn't exist)
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()

    print("loading and cleaning data...")

    # CSV_AND_JSON FILES
    # Customers
    df_customers = pd.read_csv('customers.csv')
    df_customers.to_sql('customers', conn, if_exists='replace', index=False)

    # Accounts
    df_accounts = pd.read_csv('accounts.csv')
    df_accounts.to_sql('accounts', conn, if_exists='replace', index=False)

    # Transactions
    df_transactions = pd.read_csv('transactions.csv')
    df_transactions.to_sql('transactions', conn, if_exists='replace', index=False)

    # Branches
    df_branches = pd.read_csv('branches.csv')
    df_branches.to_sql('branches', conn, if_exists='replace', index=False)

    # Loans
    df_loans = pd.read_json('loans.json')
    df_loans.to_sql('loans', conn, if_exists='replace', index=False)

    # Credit Cards
    df_credit_cards = pd.read_json('credit_cards.json')
    df_credit_cards.to_sql('credit_cards', conn, if_exists='replace', index=False)

    # support Tickets
    df_support_tickets = pd.read_json('support_tickets.json')
    df_support_tickets.to_sql('support_tickets', conn, if_exists='replace', index=False)

    print("Database 'bank.db' successfully created with tables!")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()

    