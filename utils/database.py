import mysql.connector
import pandas as pd

# def get_connection():
#     print("Success: get_connection Started")
#     return mysql.connector.connect(
#         host="localhost",           
#         user="root",       
#         password="root",   
#         database="mental_health_app"
#     )
import streamlit as st
def get_connection():
    try:
        print("Attempting to connect to the database...")
        if "db_connection" not in st.session_state:
            st.session_state.db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="mental_health_app"
            )
            print("Database connection initialized in session state.")
        else:
            print("Reusing existing connection from session state.")
        return st.session_state.db_connection
    except Exception as e:
        print(f"Error initializing database connection: {e}")
        raise


# Stackoverflow: Streamlit re-runs the entire script on every user interaction, which can lead to reinitializing the database connection unnecessarily. 
# Use st.session_state properly to prevent this.

# Function to log sentiment analysis results
# def log_sentiment(sentiment):  # This is the table for basic version
#     try:
#         connection = get_connection()
#         print("check C")
#         cursor = connection.cursor()
#         print("check A")
#         # Insert logs into the table
#         sql = "INSERT INTO sentiment_logs (sentiment) VALUES (%s)"
#         values = (sentiment,)
#         cursor.execute(sql, values)
#         print("check B")
#         connection.commit()
#         print("Log saved successfully.")
#     except mysql.connector.Error as err:
#         print(f"Error: {err}")
#     finally:
#         if connection:
#             cursor.close()
#             connection.close()


def log_sentiment(sentiment):
    try:
        print("Starting log_sentiment...")
        connection = get_connection()
        print("Connection acquired.")
        cursor = connection.cursor()
        print("Cursor created.")

        # Insert logs into the table
        sql = "INSERT INTO sentiment_logs (sentiment) VALUES (%s)"
        values = (sentiment,)
        cursor.execute(sql, values)
        print("SQL query executed.")

        connection.commit()
        print("Log saved successfully.")
    except mysql.connector.Error as err:
        print(f"Error during database operation: {err}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        if "db_connection" in st.session_state and st.session_state.db_connection.is_connected():
            print("Keeping session state connection open for reuse.")
        else:
            print("Closing unused connection.")
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
def log_emotions(emotions):    # Logs emotions and their scores to the MySQL database.
    try:
        print("Starting log_emotions...")
        connection = get_connection()
        print("Connection acquired.")
        cursor = connection.cursor()
        print("Cursor created.")

        # Insert each emotion into the database
        for emotion, score in emotions.items():
            print(f"Logging emotion: {emotion}, score: {score}")
            sql = "INSERT INTO emotion_logs (emotion, score) VALUES (%s, %s)"
            values = (emotion, score)
            cursor.execute(sql, values)

        connection.commit()
    except mysql.connector.Error as err:
        print(f"Error during database operation: {err}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        if "db_connection" in st.session_state and st.session_state.db_connection.is_connected():
            print("Keeping session state connection open for reuse.")
        else:
            print("Closing unused connection.")
            cursor.close()
            connection.close()



def fetch_weekly_emotions():
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

