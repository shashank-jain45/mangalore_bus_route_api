import sqlite3

# Step 1: Connect to the SQLite database
# Replace 'your_database.db' with the path to your actual SQLite database file
conn = sqlite3.connect('bus_routes.db')
cursor = conn.cursor()

# Query to fetch distinct strings separated by hyphen from the route column
query = """
WITH SplitStrings AS (
    SELECT DISTINCT
        TRIM(substr(route, start_pos, end_pos - start_pos)) AS split_value
    FROM
        bus_routes,
        -- Generate positions for substrings between hyphens
        (SELECT rowid, instr(route, '-', start_pos) + 1 AS start_pos, instr(route, '-', instr(route, '-', start_pos) + 1) AS end_pos FROM bus_routes) 
    WHERE
        rowid IN (SELECT rowid FROM bus_routes)
)
SELECT DISTINCT split_value FROM SplitStrings; 
"""
cursor.execute(query)

# Fetch and print the resultsyour_database
rows = cursor.fetchall()
for row in rows:
    print(row[0])

# Close the connection
conn.close()

