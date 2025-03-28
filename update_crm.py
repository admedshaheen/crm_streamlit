#!/usr/bin/env python
# coding: utf-8

# In[9]:


import sqlite3
from faker import Faker
import random

fake = Faker()

conn = sqlite3.connect('investor_crm.db')
cursor = conn.cursor()

def generate_investor(id_start):
    return {
        'investor_id': id_start,
        'investor_name': fake.company(),
        'investor_type': random.choice(["VC", "Private Equity", "Institutional Investor", "Family Office"]),
        'sector_focus': random.choice(['Fintech', 'Healthtech', 'AI', 'Consumer Goods', 'Edtech', 'E-commerce', 'SaaS', 'Biotech']),
        'check_size_usd': random.randint(100000, 5000000),
        'investment_stage': random.choice(['Seed', 'Series A', 'Series B', 'Series C']),
        'investment_frequency': random.randint(1, 12),
        'geographic_focus': random.choice(['North America', 'Europe', 'MENA', 'Asia', 'Global']),
        'last_investment_date': str(fake.date_between('-30d', 'today'))
    }

current_max_id = cursor.execute('SELECT MAX(investor_id) FROM investors').fetchone()[0] or 1000

new_investors = [generate_investor(current_max_id + i + 1) for i in range(5)]

# Clearly specify the columns to avoid the error
for investor in new_investors:
    cursor.execute('''
    INSERT INTO investors (
        investor_id, investor_name, investor_type, sector_focus,
        check_size_usd, investment_stage, investment_frequency,
        geographic_focus, last_investment_date
    ) VALUES (
        :investor_id, :investor_name, :investor_type, :sector_focus, 
        :check_size_usd, :investment_stage, :investment_frequency, 
        :geographic_focus, :last_investment_date
    )
    ''', investor)

conn.commit()
conn.close()

print("✅ CRM successfully updated with 5 new investors!")


# In[ ]:




