import sqlite3

# Connect to the SQLite3 database
conn = sqlite3.connect("data.db")
c = conn.cursor()

# Retrieve all the data from the table
c.execute("SELECT * FROM data")
rows = c.fetchall()

# Print the data
for row in rows:
    print(row)

# Close the database connection
conn.close()