import sqlite3

# Step 1: Define your function to insert frame data
def insert_frame_data(conn, video_id, frame_number, timestamp, file_path):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO frames (video_id, frame_number, timestamp, file_path)
        VALUES (?, ?, ?, ?)
    ''', (video_id, frame_number, timestamp, file_path))
    conn.commit()

# Step 2: Establish the connection to your SQLite database
conn = sqlite3.connect('videos.db')

# Clear the frames table (delete all existing data)
cursor = conn.cursor()
cursor.execute("DELETE FROM frames")
conn.commit()

# Step 3: Insert some test data
insert_frame_data(conn, 1, 1, 0.0, 'frame1.jpg')
insert_frame_data(conn, 1, 2, 0.033, 'frame2.jpg')

# Step 4: Fetch and display all data from the frames table
cursor.execute("SELECT * FROM frames")
rows = cursor.fetchall()

print("Data in the frames table:")
for row in rows:
    print(row)

# Step 5: Close the connection after operations are done
conn.close()
