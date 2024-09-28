import sqlite3

def check_tables(db_path='videos.db'):
    """Check and print the tables in the database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query to get the list of tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Print the tables
    if tables:
        print("Tables in the database:")
        for table in tables:
            print(table[0])
    else:
        print("No tables found in the database.")

    # Close the connection
    conn.close()

if __name__ == '__main__':
    check_tables()
