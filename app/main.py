import streamlit as st
import sys, os
# Add the project's root directory to sys.path - resolving path 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the modules
from app.generate_report import generate_report
import app.write_your_mood_basic as basic
import app.write_your_mood_pro as pro
import app.cognitive_corrections as cognitive

def main():
    st.sidebar.title("Mental Health Analytics App")
    st.sidebar.write("Choose a feature:")
    feature = st.sidebar.radio("Features", ["Write Your Mood", "Cognitive Corrections"])

    if feature == "Write Your Mood":
        st.sidebar.write("Choose a version:")
        version = st.sidebar.radio("Version", ["Basic", "Pro"])

        if version == "Basic":
            basic.main()
            st.sidebar.subheader("Visualizations for Basic")
            if st.sidebar.button("Show Sentiment Trends", key="basic_sentiment_trends"):
                basic.visualize_sentiment_trends()
        elif version == "Pro":
            pro.main()
            st.sidebar.subheader("Visualizations for Pro")
            if st.sidebar.button("Show Weekly Emotion Trends", key="pro_weekly_trends"):
                pro.visualize_weekly_emotions()

    elif feature == "Cognitive Corrections":
        cognitive.main()
        st.sidebar.subheader("Visualizations for Cognitive Corrections")
        if st.sidebar.button("View Recurring Themes", key="cognitive_recurring_themes"):
            cognitive.visualize_recurring_themes()
    
    st.sidebar.subheader("Reports Section")
    if st.sidebar.button("Generate Report for Doctor"):
        try:
            generate_report()
            with open("data/patient_report.pdf", "rb") as pdf_file:
                st.sidebar.download_button(
                label="Download Report",
                data=pdf_file,
                file_name="patient_report.pdf",
                mime="application/pdf"
                )
            st.success("Report generated successfully!")
        except Exception as e:
            st.error(f"Failed to generate the report: {e}")




if __name__ == "__main__":
    main()
