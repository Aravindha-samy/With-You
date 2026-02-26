import sqlite3
import datetime

def initialize_database(db_name='withyou.db'):
    """
    Initializes the SQLite database and creates the necessary tables.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER,
        diagnosis_stage TEXT,
        location TEXT
    )
    ''')

    # Create Relationships table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Relationships (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        name TEXT NOT NULL,
        relationship_type TEXT,
        description TEXT,
        importance_level INTEGER,
        photo_reference TEXT,
        FOREIGN KEY (user_id) REFERENCES Users (id)
    )
    ''')

    # Create Events table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Events (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        event_description TEXT NOT NULL,
        event_date TEXT,
        event_time TEXT,
        FOREIGN KEY (user_id) REFERENCES Users (id)
    )
    ''')

    # Create Interactions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Interactions (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        timestamp TEXT,
        question TEXT,
        emotional_tone_marker TEXT,
        repetition_count INTEGER,
        FOREIGN KEY (user_id) REFERENCES Users (id)
    )
    ''')

    # Create CognitiveMetrics table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS CognitiveMetrics (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        date TEXT,
        orientation_frequency INTEGER,
        anxiety_average REAL,
        repetition_patterns INTEGER,
        escalation_flags INTEGER,
        FOREIGN KEY (user_id) REFERENCES Users (id)
    )
    ''')

    conn.commit()
    conn.close()

def insert_mock_data(db_name='withyou.db'):
    """
    Inserts mock data into the database.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Insert a sample user
    cursor.execute("INSERT INTO Users (id, name, age, diagnosis_stage, location) VALUES (?, ?, ?, ?, ?)",
                   (1, 'Raj', 78, 'Early-stage', "You're at home, in your safe and comfortable space."))

    # Insert a sample event
    today = datetime.date.today().strftime("%Y-%m-%d")
    cursor.execute("INSERT INTO Events (user_id, event_description, event_date, event_time) VALUES (?, ?, ?, ?)",
                   (1, "Your daughter, Anna, is visiting this afternoon.", today, "15:00"))

    conn.commit()
    conn.close()


if __name__ == '__main__':
    db_file = 'withyou.db'
    initialize_database(db_file)
    insert_mock_data(db_file)
    print(f"Database '{db_file}' initialized and mock data inserted successfully.")
