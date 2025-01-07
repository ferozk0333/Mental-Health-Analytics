import mysql.connector
import pandas as pd

def get_connection():
    return mysql.connector.connect(
        host="localhost",           
        user="root",       
        password="root",   
        database="mental_health_app"
    )

# Function to log sentiment analysis results
def log_sentiment(sentiment):  # This is the table for basic version
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Insert logs into the table
        sql = "INSERT INTO sentiment_logs (sentiment) VALUES (%s)"
        values = (sentiment,)
        cursor.execute(sql, values)

        connection.commit()
        print("Log saved successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection:
            cursor.close()
            connection.close()

# Fetch sentiment logs from the database
def fetch_sentiment_logs_with_time():
    try:
        connection = get_connection()
        query = """
        SELECT sentiment, YEARWEEK(created_at, 1) AS week, TIME(created_at) AS time
        FROM sentiment_logs
        """
        logs = pd.read_sql(query, connection)
        return logs
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        if connection:
            connection.close()

# Creating table for pro verson
def log_emotions(emotions):
    """
    Logs emotions and their scores to the MySQL database.
    :param emotions: Dictionary of emotions and their scores.
    """
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Insert each emotion into the database
        for emotion, score in emotions.items():
            sql = "INSERT INTO emotion_logs (emotion, score) VALUES (%s, %s)"
            values = (emotion, score)
            cursor.execute(sql, values)

        connection.commit()
        print("Emotion logs saved successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection:
            cursor.close()
            connection.close()


def fetch_weekly_emotions():
    """
    Fetch the sum of emotion scores grouped by week from the database.
    :return: DataFrame with the sum of emotion scores grouped by week.
    """
    try:
        connection = get_connection()
        query = """
        SELECT 
            emotion, 
            YEARWEEK(created_at, 1) AS week, 
            SUM(score) AS total_score
        FROM emotion_logs
        GROUP BY week, emotion
        ORDER BY week;
        """
        logs = pd.read_sql(query, connection)
        return logs
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        if connection:
            connection.close()


# For cognitive corrections - Logs a thought's category and timestamp into the database.
def log_category(categories):
    print("Check A")
    try:
        print("Check B")
        connection = get_connection()
        print("Check C: Connection established")
        cursor = connection.cursor()
        print("Check D: Cursor created")

        for category in categories:
            print(f"Logging category: {category}")
            sql = "INSERT INTO thought_logs (category) VALUES (%s)"
            values = (category,)
            cursor.execute(sql, values)

        connection.commit()
        print("Thoughts logged successfully to DB.")
    except Exception as e:
        print(f"Error while logging thoughts to DB: {e}")
    finally:
        if 'connection' in locals() and connection:
            print("Closing connection.")
            cursor.close()
            connection.close()

