import datetime
import sqlite3

def get_current_date():
    """Returns the current date, formatted."""
    return datetime.date.today().strftime("%A, %B %d, %Y")

def get_current_time():
    """Returns the current time, formatted."""
    return datetime.datetime.now().strftime("%I:%M %p")

def get_user_location(user_id, db_name='withyou.db'):
    """
    Retrieves the user's location from the database.
    
    :param user_id: The ID of the user.
    :param db_name: The name of the database file.
    :return: The user's location as a string.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT location FROM Users WHERE id = ?", (user_id,))
    location_row = cursor.fetchone()
    conn.close()
    return location_row[0] if location_row else "You're in a safe place."

def get_todays_events(user_id, db_name='withyou.db'):
    """
    Retrieves today's events for a given user from the database.

    :param user_id: The ID of the user.
    :param db_name: The name of the database file.
    :return: A string describing today's events.
    """
    today = datetime.date.today().strftime("%Y-%m-%d")
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT event_description FROM Events WHERE user_id = ? AND event_date = ?", (user_id, today))
    event_rows = cursor.fetchall()
    conn.close()
    
    if event_rows:
        return " and ".join([row[0] for row in event_rows])
    else:
        return "No specific events are scheduled for today."
