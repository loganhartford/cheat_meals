import sqlite3
import pandas as pd

# Read the CSV file into a pandas DataFrame
df = pd.read_csv("data/fastfood.csv")

# Create a SQLite database and connect to it
conn = sqlite3.connect("data/fastfood.db")

# Save the DataFrame to the database
df.to_sql("nutrition", conn, if_exists="replace", index=False)

# Close the database connection
conn.close()

if __name__ == "__main__":
    conn = sqlite3.connect("data/fastfood.db")
    # Retrieve data from the table into a pandas DataFrame
    select_data_query = "SELECT * FROM nutrition"
    df = pd.read_sql_query(select_data_query, conn)
    # Close the database connection
    conn.close()

    print(df)
