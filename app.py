#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import sqlite3

# Connect to your database
conn = sqlite3.connect('investor_crm.db')
cursor = conn.cursor()

# Function to query investors
def get_investors(sector, stage):
    query = '''
    SELECT investor_name, investor_type, check_size_usd, geographic_focus, last_investment_date
    FROM investors
    WHERE sector_focus=? AND investment_stage=?
    '''
    return pd.read_sql_query(query, conn, params=(sector, stage))

# Function to add new investor
def add_investor(investor_id, name, type_, sector, check_size, stage, frequency, geography, date):
    cursor.execute('''
    INSERT INTO investors VALUES (?,?,?,?,?,?,?,?,?)
    ''', (investor_id, name, type_, sector, check_size, stage, frequency, geography, date))
    conn.commit()

# Streamlit Interface clearly designed
st.title("🚀 Investor CRM System")

menu = ["View Investors", "Add Investor"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "View Investors":
    st.subheader("🔍 Query Investors")
    sector = st.selectbox('Sector', ['Fintech', 'Healthtech', 'AI', 'Consumer Goods', 'Edtech', 'E-commerce', 'SaaS', 'Biotech'])
    stage = st.selectbox('Stage', ['Seed', 'Series A', 'Series B', 'Series C'])
    
    if st.button('Search'):
        results = get_investors(sector, stage)
        st.dataframe(results)

elif choice == "Add Investor":
    st.subheader("➕ Add New Investor")

    investor_id = st.number_input("Investor ID", min_value=1000)
    name = st.text_input("Investor Name")
    type_ = st.selectbox("Investor Type", ["VC", "Private Equity", "Institutional Investor", "Family Office"])
    sector = st.selectbox("Sector Focus", ['Fintech', 'Healthtech', 'AI', 'Consumer Goods', 'Edtech', 'E-commerce', 'SaaS', 'Biotech'])
    check_size = st.number_input("Check Size (USD)", min_value=50000)
    stage = st.selectbox("Investment Stage", ['Seed', 'Series A', 'Series B', 'Series C'])
    frequency = st.number_input("Investment Frequency per year", min_value=1, max_value=20)
    geography = st.selectbox("Geographic Focus", ['North America', 'Europe', 'MENA', 'Asia', 'Global'])
    date = st.date_input("Last Investment Date")

    if st.button("Add Investor"):
        add_investor(investor_id, name, type_, sector, check_size, stage, frequency, geography, date)
        st.success(f"Investor '{name}' added successfully!")

conn.close()

