
# UBER SUPPLY-DEMAND GAP ANALYSIS - PYTHON SCRIPT

# 1. Import Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
from datetime import datetime

# 2. Load & Clean Dataset
df = pd.read_csv("Uber Request Data.csv")

df['Request timestamp'] = pd.to_datetime(df['Request timestamp'], errors='coerce')
df['Drop timestamp'] = pd.to_datetime(df['Drop timestamp'], errors='coerce')
df = df.dropna(subset=['Request timestamp'])

df['Request hour'] = df['Request timestamp'].dt.hour

def get_time_slot(hour):
    if pd.isna(hour): return 'Unknown'
    elif 0 <= hour < 4: return 'Late Night'
    elif 4 <= hour < 8: return 'Early Morning'
    elif 8 <= hour < 12: return 'Morning'
    elif 12 <= hour < 16: return 'Afternoon'
    elif 16 <= hour < 20: return 'Evening'
    else: return 'Night'

df['Time slot'] = df['Request hour'].apply(get_time_slot)

df['Status'] = df['Status'].astype(str).str.strip().str.title()
df['Pickup point'] = df['Pickup point'].astype(str).str.strip().str.title()
df = df.dropna(subset=['Status', 'Pickup point'])

# 3. Load into SQLite
conn = sqlite3.connect(":memory:")
df.to_sql("uber_data", conn, index=False, if_exists="replace")

# 4. Generate Visualizations

# Chart 1: Requests by Time Slot
df['Time slot'].value_counts().reindex(
    ['Late Night', 'Early Morning', 'Morning', 'Afternoon', 'Evening', 'Night']
).plot(kind='bar', color='skyblue', edgecolor='black')
plt.title("Total Requests by Time Slot")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Chart 2: Status by Time Slot
query = """
SELECT [Time slot], Status, COUNT(*) AS total
FROM uber_data
GROUP BY [Time slot], Status
"""
result = pd.read_sql(query, conn)
plt.figure(figsize=(12, 6))
sns.barplot(data=result, x='Time slot', y='total', hue='Status', palette='Set2')
plt.title("Status Distribution Across Time Slots")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Chart 3: Status by Pickup Point
query = """
SELECT [Pickup point], Status, COUNT(*) AS total
FROM uber_data
GROUP BY [Pickup point], Status
"""
df3 = pd.read_sql(query, conn)
sns.barplot(data=df3, x='Pickup point', y='total', hue='Status', palette='pastel')
plt.title("Request Status by Pickup Point")
plt.tight_layout()
plt.show()

# Chart 4: Completed Trips Heatmap
query = """
SELECT [Pickup point], [Time slot], COUNT(*) AS total
FROM uber_data
WHERE Status = 'Trip Completed'
GROUP BY [Pickup point], [Time slot]
"""
df4 = pd.read_sql(query, conn)
pivot = df4.pivot(index='Pickup point', columns='Time slot', values='total').fillna(0)
sns.heatmap(pivot, annot=True, fmt='d', cmap='YlGnBu')
plt.title("Completed Trips Heatmap")
plt.tight_layout()
plt.show()

# Chart 5: Hourly Requests
query = """
SELECT [Request hour] AS hour, COUNT(*) AS total
FROM uber_data
GROUP BY hour
ORDER BY hour
"""
df5 = pd.read_sql(query, conn)
sns.barplot(data=df5, x='hour', y='total', color='coral')
plt.title("Requests by Hour")
plt.tight_layout()
plt.show()

# Chart 6: Ride Status Pie Chart
query = """
SELECT Status, COUNT(*) AS total
FROM uber_data
GROUP BY Status
"""
df6 = pd.read_sql(query, conn)
plt.pie(df6['total'], labels=df6['Status'], autopct='%1.1f%%', colors=sns.color_palette("pastel"))
plt.title("Ride Status Breakdown")
plt.show()

# Chart 7: Cancellations by Time Slot
query = """
SELECT [Time slot], COUNT(*) AS cancelled
FROM uber_data
WHERE Status = 'Cancelled'
GROUP BY [Time slot]
"""
df7 = pd.read_sql(query, conn)
sns.barplot(data=df7, x='Time slot', y='cancelled', color='salmon')
plt.title("Cancellations by Time Slot")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Chart 8: No Cars Available by Time Slot
query = """
SELECT [Time slot], COUNT(*) AS no_cars
FROM uber_data
WHERE Status = 'No Cars Available'
GROUP BY [Time slot]
"""
df8 = pd.read_sql(query, conn)
sns.barplot(data=df8, x='Time slot', y='no_cars', color='slateblue')
plt.title("No Cars Available by Time Slot")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Chart 9: Completion Rate by Time Slot
query = """
SELECT [Time slot] AS slot,
       ROUND(SUM(CASE WHEN Status = 'Trip Completed' THEN 1 ELSE 0 END)*1.0 / COUNT(*), 2) AS completion_rate
FROM uber_data
GROUP BY [Time slot]
"""
df9 = pd.read_sql(query, conn)
sns.barplot(data=df9, x='slot', y='completion_rate', color='mediumseagreen')
plt.title("Trip Completion Rate by Time Slot")
plt.ylim(0, 1)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
