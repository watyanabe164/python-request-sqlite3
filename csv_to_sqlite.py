import csv
import sqlite3
import urllib.request

# Download the CSV data from the URL
url = "https://www.mhlw.go.jp/content/001060467.csv"
response = urllib.request.urlopen(url)
data = response.read().decode("utf-8")

# Parse the CSV data and store it in a list of tuples
rows = []
for row in csv.reader(data.splitlines()):
    rows.append(tuple(row))

# Connect to the SQLite3 database and create a table
conn = sqlite3.connect("data.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS data (date TEXT, cases INTEGER)")

# Insert the data into the table
c.executemany("INSERT INTO data VALUES (?, ?)", rows)
conn.commit()

# Close the database connection
conn.close()