import streamlit as st
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import sys, os
import pandas as pd

# Add the project's root directory to sys.path - I ahve done this to resolve path issue
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.database import log_category, log_sentiment
from db.db_config import initialize_sqlite_db, log_category_to_sqlite, fetch_recurring_themes
initialize_sqlite_db()


# Let's Load model and vectorizer
@st.cache_resource
def load_classifier():
    with open('models/thought_classifier.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('models/thought_vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    return model, vectorizer

# Classify thoughts
def classify_thoughts(thoughts, model, vectorizer):
    thoughts_vec = vectorizer.transform(thoughts)
    categories = model.predict(thoughts_vec)
    return categories

# Visualizations for the CBT model
def visualize_categories(categories):
    category_counts = pd.Series(categories).value_counts()

    # Bar Chart
    st.subheader("Category Distribution")
    plt.figure(figsize=(8, 4))
    sns.barplot(x=category_counts.index, y=category_counts.values, palette="Set2")
    plt.title("Thought Categorization Results")
    plt.xlabel("Categories")
    plt.ylabel("Number of Thoughts")
    st.pyplot(plt.gcf())

    # Pie Chart
    st.subheader("Category Distribution Pie Chart")
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(category_counts.values, labels=category_counts.index, autopct='%1.1f%%', colors=sns.color_palette('Set2'))
    ax.set_title("Thought Categorization Pie Chart")
    st.pyplot(fig)




# Displaying by Fetching  and visualizing recurring themes
def visualize_recurring_themes():
    recurring_themes = fetch_recurring_themes()
    if not recurring_themes.empty:
        st.subheader("Recurring Themes Over Time")
        # Plot bar chart
        plt.figure(figsize=(8, 5))
        sns.barplot(data=recurring_themes, x='category', y='count', palette="Set2")
        plt.title("Top Recurring Thought Categories")
        plt.xlabel("Categories")
        plt.ylabel("Count")
        plt.xticks(rotation=45)
        st.pyplot(plt.gcf())



# Streamlit App to make the Front End
def main():
    st.title("Cognitive Corrections")
    st.write("Classify thoughts into categories to identify recurring themes.")
    st.write("Based on Cognitive Behavioural Theory (CBT), this feature helps you identify the most bothering thoughts. Enter up to 5 thoughts or ideas on your mind at this moment.")
    # Load classifier
    model, vectorizer = load_classifier()

    # Input thoughts
    thoughts = []
    for i in range(1, 6):
        thought = st.text_input(f"Thought {i}:")
        if thought.strip():
            thoughts.append(thought)

    if st.button("Classify Thoughts"):
        if thoughts:
            categories = classify_thoughts(thoughts, model, vectorizer)
            st.write("Classification Results:")
            for i, category in enumerate(categories):
                st.write(f"**Thought {i + 1}:** {category}")
            
            # try:
            # # Log categories into the database
            #     print(categories[0])
            #     log_category(categories)
                
            #     st.success("Thoughts have been logged successfully!")
            # except Exception as e:
            #     st.error(f"Failed to log thoughts: {e}")

            # Log categories into SQLite
            try:
                log_category_to_sqlite(categories)
                st.success("Categories logged to DB successfully!")
            except Exception as e:
                st.error(f"Failed to log categories: {e}")


            # Visualize category distribution
            visualize_categories(categories)
            
        else:
            st.error("Please enter at least one thought to classify.")

    # Button for recurring themes
    if st.button("View Recurring Themes"):
        visualize_recurring_themes()

if __name__ == "__main__":
    main()