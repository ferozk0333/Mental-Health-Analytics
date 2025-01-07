import streamlit as st
from transformers import pipeline
import matplotlib.pyplot as plt
import seaborn as sns
import sys, os
# Add the project's root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.database import log_emotions, fetch_weekly_emotions

# Load the emotion classification model
@st.cache_resource
def load_emotion_model():
    return pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion", top_k=None)

# Analyze emotions dinction that will run later
def analyze_emotions(text, model):
    results = model(text)  # Get the emotion classification results
    # Process the first list of results to extract emotions and scores
    emotion_scores = {res['label']: res['score'] for res in results[0]}
    return emotion_scores



# Visualize emotion distribution
def visualize_emotions(emotion_scores):
    emotions = list(emotion_scores.keys())
    scores = list(emotion_scores.values())

    # Bar Chart
    plt.figure(figsize=(8, 4))
    sns.barplot(x=emotions, y=scores, palette="Set2", dodge=False, legend=False)
    plt.title("Emotion Distribution")
    plt.xlabel("Emotions")
    plt.ylabel("Scores")
    st.pyplot(plt.gcf())

    # Radar Chart to undestand major emotions
    st.write("Radar Chart to Understand Major Emotions")
    try:
        import plotly.graph_objects as go
        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=scores,
            theta=emotions,
            fill='toself',
            name='Emotion Scores'
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )
            ),
            showlegend=False
        )
        st.plotly_chart(fig)
    except ImportError:
        st.error("Plotly is not installed for radar charts. Skipping this visualization.")

# Weekly report
def visualize_weekly_emotions():
    logs = fetch_weekly_emotions()  # Fetch weekly emotion data
    if logs is not None and not logs.empty:
        st.subheader("Weekly Emotion Trends")
        st.write("This chart shows the total intensity of emotions logged each week.")

        # Convert week column to string for better readability
        logs['week'] = logs['week'].astype(str)

        # Weekly bar chart
        plt.figure(figsize=(12, 6))
        sns.barplot(data=logs, x='week', y='total_score', hue='emotion', palette="Set2")
        plt.title("Weekly Emotion Trends (Summed Scores)")
        plt.xlabel("Week")
        plt.ylabel("Total Emotion Score")
        plt.xticks(rotation=45)
        st.pyplot(plt.gcf())

        # Pie chart for a specific week
        st.subheader("Emotion Distribution for a Specific Week")
        selected_week = st.selectbox("Select a Week", logs['week'].unique())
        if selected_week:
            week_data = logs[logs['week'] == selected_week]
            if not week_data.empty:
                fig, ax = plt.subplots(figsize=(6, 6))
                ax.pie(week_data['total_score'], labels=week_data['emotion'], autopct='%1.1f%%', colors=sns.color_palette('Set2'))
                ax.set_title(f"Emotion Distribution for Week {selected_week}")
                st.pyplot(fig)
            else:
                st.write("No emotion data available for the selected week.")
    else:
        st.write("No emotion logs available for visualization.")


# Streamlit App - main body
def main():
    st.title("Write Your Mood - Pro Version")
    st.write("This version analyzes the emotions in your text using a pre-trained model.")
    
    # Load emotion classification model
    emotion_model = load_emotion_model()

    # Input text
    text_input = st.text_area("Describe your mood or day:")

    # Analyze button when pressed
    if st.button("Analyze"):
        if text_input.strip():
            emotion_scores = analyze_emotions(text_input, emotion_model)
            st.subheader("Emotion Analysis Results")
            st.write(emotion_scores)

            # Log emotions to MySQL dtabase at the backend
            log_emotions(emotion_scores)

            # Visualize emotion distributions
            visualize_emotions(emotion_scores)
            st.success("Emotion analysis results have been logged successfully!")
        else:
            st.error("Please enter some text to analyze.")

if __name__ == "__main__":
    main()
