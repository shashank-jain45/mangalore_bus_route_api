import pandas as pd
import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("bus_routes.db")
cursor = conn.cursor()

# Load CSV data into a DataFrame
csv_file = "bus_routes.csv"
df = pd.read_csv(csv_file)

# Assuming your CSV has columns: 'bus_number', 'from_location', 'to_location', 'route'
# Rename columns if necessary to match your database schema
df.columns = ["bus_number", "from_location", "to_location", "route"]

# Write the DataFrame to an SQLite table (replace table name as needed)
df.to_sql("bus_routes", conn, if_exists="replace", index=False)

print("Data imported successfully.")

# Close the connection
conn.close()
