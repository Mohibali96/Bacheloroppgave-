import mysql.connector

# Funksjon for å koble til MySQL-databasen
def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="reidar12",       
            password="Bachelor10!",       
            database="sports_event_detection"
        )
        print("Tilkobling til databasen var vellykket.")  # Bekreftelsesmelding hvis tilkoblingen lykkes
        return conn
    except mysql.connector.Error as err:
        print(f"Feil ved tilkobling til databasen: {err}")
        return None  # Returner None hvis tilkoblingen mislykkes

# Funksjon for å opprette tabellene
def create_tables():
    conn = connect_to_database()
    if conn is not None:  # Fortsett bare hvis tilkoblingen er vellykket
        cursor = conn.cursor()

        # Opprett Videos-tabellen
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Videos (
                video_id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                file_path TEXT NOT NULL,
                duration FLOAT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Opprett Transcriptions-tabellen
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

        conn.commit()
        conn.close()
        print("Tabellene ble opprettet.")
    else:
        print("Kunne ikke opprette tabeller fordi tilkoblingen til databasen mislyktes.")

# Kjør funksjonen for å opprette tabellene hvis denne filen kjøres direkte
if __name__ == "__main__":
    # Test tilkoblingen
    try:
        conn = connect_to_database()
        if conn:
            print("Tilkobling til databasen var vellykket.")
    except mysql.connector.Error as err:
        print(f"Feil ved tilkobling til databasen: {err}")

    # Opprett tabellene
    create_tables()
