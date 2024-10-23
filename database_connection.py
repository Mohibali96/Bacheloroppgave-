# -*- coding: utf-8 -*-

import mysql.connector

# Function to connect to the MySQL database
def connect_to_database():
    try:
        print("Trying to connect to the database...")  # Debug 
        conn = mysql.connector.connect(
            host="localhost",
            user="Reidar12",         
            password="Bachelor10!",   
            database="sports_clips"   
        )
        print("Connection to the database was successful.")  # Confirmation message if connection succeeds
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to the database: {err}")
        return None  # Return None if the connection fails

# Function to create the tables
def create_tables():
    print("Starting table creation...")  # Debug
    conn = connect_to_database()
    if conn is not None:  # Proceed only if the connection is successful
        print("Connection is not None, proceeding with table creation.")
        cursor = conn.cursor()

        # Create the Videos table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Videos (
                video_id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                file_path TEXT NOT NULL,
                duration FLOAT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("The Videos table was created or already exists.")  # Confirmation message

        # Create the Transcriptions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Transcriptions (
                transcription_id INT AUTO_INCREMENT PRIMARY KEY,
                video_id INT,
                start_time FLOAT,
                end_time FLOAT,
                text TEXT,
                FOREIGN KEY (video_id) REFERENCES Videos(video_id) ON DELETE CASCADE
            )
        ''')
        print("The Transcriptions table was created or already exists.")  # Confirmation message

        conn.commit()
        conn.close()
        print("Tables were created and the connection is closed.")
    else:
        print("Could not create tables because the connection to the database failed.")

# Function to insert data into the Videos table
def insert_video_data(title, file_path, duration):
    conn = connect_to_database()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Videos (title, file_path, duration)
            VALUES (%s, %s, %s)
        ''', (title, file_path, duration))
        conn.commit()
        print(f"Video titled '{title}' was inserted.")
        conn.close()
    else:
        print("Could not connect to the database to insert data.")

# Test to insert your video
if __name__ == "__main__":
    print("Running database_connection.py...")  # Debug message
    create_tables()  # Create tables if necessary

    # Insert your video with title, file path, and duration
    insert_video_data("")

    print("Finished running database_connection.py")  # Confirmation message

