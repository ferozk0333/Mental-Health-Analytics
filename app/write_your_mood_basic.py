import streamlit as st
import pickle
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
import re
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.database import log_sentiment, fetch_sentiment_logs_with_time  # Import database logging function, fetching function
import matplotlib.pyplot as plt
import pandas as pd


# Download NLTK musts
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

# Load trained model and vectorizer
with open('models/sentiment_model.pkl', 'rb') as f:
    sentiment_model = pickle.load(f)

with open('models/vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

# Initialize preprocessing tools
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Preprocessing function for text
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    return " ".join(tokens)

# Sentiment analysis function
def analyze_sentiment(text):
    cleaned_text = preprocess_text(text)
    vectorized_text = vectorizer.transform([cleaned_text])
    sentiment = sentiment_model.predict(vectorized_text)[0]
    return sentiment

import seaborn as sns
import matplotlib.pyplot as plt

# Helper function to calculate mean time
def calculate_mean_time(logs, sentiment_type):
    sentiment_data = logs[logs['sentiment'] == sentiment_type]
    if not sentiment_data.empty:
        try:
            # Ensure 'time' column is of proper format
            sentiment_data['time'] = pd.to_timedelta(sentiment_data['time'])
            mean_time = sentiment_data['time'].mean()
            return (pd.Timestamp("1900-01-01") + mean_time).time()  # Convert to time format
        except Exception as e:
            print(f"Error processing mean time for {sentiment_type}: {e}")
            return None
    return None

# Helper function for creating time buckets
def assign_time_bucket(time_str):
    # Check if the input is a timedelta
    if isinstance(time_str, pd.Timedelta):
        # Extract time portion from Timedelta
        time = (pd.Timestamp("1900-01-01") + time_str).time()
    else:
        # Convert string to datetime and extract time
        time = pd.to_datetime(time_str).time()
    
    # Assign time buckets using If Else statemetns
    if time >= pd.to_datetime("06:00:00").time() and time < pd.to_datetime("12:00:00").time():
        return "Morning"
    elif time >= pd.to_datetime("12:00:00").time() and time < pd.to_datetime("18:00:00").time():
        return "Afternoon"
    elif time >= pd.to_datetime("18:00:00").time() and time < pd.to_datetime("22:00:00").time():
        return "Evening"
    else:
        return "Night"

    
# Visualization function
def visualize_sentiment_trends():
    logs = fetch_sentiment_logs_with_time()
    if logs is not None and not logs.empty:
        # Convert week column to string for better readability
        logs['week'] = logs['week'].astype(str)

        # Weekly bar chart
        st.subheader("Weekly Sentiment Trends")
        st.write("This chart shows the distribution of sentiments logged over weeks.")
        weekly_logs = logs.groupby(['week', 'sentiment']).size().reset_index(name='count')
        plt.figure(figsize=(12, 6))
        sns.barplot(data=weekly_logs, x='week', y='count', hue='sentiment', palette='Set2')
        plt.title("Sentiment Trends Over Weeks")
        plt.xlabel("Week (YearWeek Format)")
        plt.ylabel("Count")
        plt.xticks(rotation=45)
        st.pyplot(plt.gcf())

        # Mean time calculations
        mean_positive_time = calculate_mean_time(logs, 'positive')
        mean_negative_time = calculate_mean_time(logs, 'negative')

        # Display mean times
        st.subheader("Mean Entry Times")
        st.write(f"**Mean time of positive sentiment entries:** {mean_positive_time if mean_positive_time else 'No data'}")
        st.write(f"**Mean time of negative sentiment entries:** {mean_negative_time if mean_negative_time else 'No data'}")

        # Assign time buckets
        logs['time_bucket'] = logs['time'].apply(assign_time_bucket)
        
        # Bar plot for sentiment distribution by time bucket
        plt.figure(figsize=(8, 6))
        sns.countplot(data=logs, x='time_bucket', hue='sentiment', palette='Set2')
        plt.title("Sentiment Distribution by Time Bucket")
        plt.xlabel("Time Bucket")
        plt.ylabel("Count")
        plt.savefig("data/mood_chart.png")
        st.pyplot(plt.gcf())

        # Pie chart for a specific week that will heop doctor understand nuanced details
        selected_week = st.selectbox("Select a Week to View Sentiment Distribution", logs['week'].unique())
        if selected_week:
            week_data = weekly_logs[weekly_logs['week'] == selected_week]
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.pie(week_data['count'], labels=week_data['sentiment'], autopct='%1.1f%%', colors=sns.color_palette('Set2'))
            ax.set_title(f"Sentiment Distribution for Week {selected_week}")
            st.pyplot(fig)
    else:
        st.write("No sentiment logs available for visualization.")

# Streamlit app mian body
def main():
    st.title("Write Your Mood - Basic Version")
    st.write("This feature allows you to share your thoughts, analyze their sentiment, and track trends over time.")
    
    # Input for user text
    text_input = st.text_area("How are you feeling today? Describe your day:")
    
    # Analyze button
    if st.button("Analyze"):
        if text_input.strip():  # Check if input is not empty
            sentiment = analyze_sentiment(text_input)
            
            # Log only the sentiment in MySQL
            log_sentiment(sentiment)
            
            st.subheader("Analysis Result")
            st.write(f"The sentiment of your text is **{sentiment}**.")
            st.success("Your sentiment analysis result has been logged successfully!")
        else:
            st.error("Please enter some text to analyze.")


if __name__ == "__main__":
    main()
