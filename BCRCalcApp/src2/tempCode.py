import sqlite3

def read_top_10_rows(db_file):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    try:
        # Replace 'your_table_name' with the actual name of your table
        table_name = 'BidItemPriceTxDot'
        
        # Query to select the top 10 rows from the table
        query = f"SELECT * FROM {table_name} LIMIT 10"
        
        # Execute the query
        cursor.execute(query)
        
        # Fetch all the rows returned by the query
        rows = cursor.fetchall()
        
        # Display the top 10 rows
        for row in rows:
            print(row)
            
    except sqlite3.Error as e:
        print("Error reading data from the database:", e)

    finally:
        # Close the database connection
        conn.close()

# Call the function and provide the path to your SQLite database file
db_file = './BenefitCostRatioApp.db'
read_top_10_rows(db_file)
