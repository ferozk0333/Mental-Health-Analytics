# This module contains logic that will generate reports for the doctor to review.

import pandas as pd
import sys, os, sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

# Add the project's root directory to sys.path - Again resolving path focus
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.database import get_connection, fetch_sentiment_logs_with_time, fetch_weekly_emotions
from db.db_config import fetch_recurring_themes



def generate_cognitive_chart(cognitive_data): # Generate a pie chart for cognitive categories and save it as an image.

    plt.figure(figsize=(6, 6))
    plt.pie(cognitive_data['count'], labels=cognitive_data['category'], autopct='%1.1f%%', startangle=140, colors=sns.color_palette("Set2"))
    plt.title("Cognitive Thought Categories")
    plt.savefig("data/cognitive_chart.png")
    plt.close()

from fpdf import FPDF

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Patient Report', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_report():
    # Fetch data
    cognitive_data = fetch_recurring_themes()     # Add parentheses to call the function

    # Generate chart
    generate_cognitive_chart(cognitive_data)

# Create PDF
    pdf = PDFReport()
    pdf.add_page()

# Add introduction
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, "This report summarizes the patient's mental health data, including mood trends and cognitive thought patterns.")

# Add mood chart
    pdf.set_font("Arial", size=12, style='B')
    pdf.cell(0, 10, "Mood Trends:", ln=True)
    pdf.image("data/mood_chart.png", x=10, y=40, w=130) 
    pdf.ln(93)  # Spacing to avoid overlapping

# Add cognitive chart
    pdf.set_font("Arial", size=12, style='B')
    pdf.cell(0, 10, "Patient's dominant thoughts are in the following categories:", ln=True)
    pdf.image("data/cognitive_chart.png", x=10, y=150, w=130) 

# Save PDF
    pdf.output("data/patient_report.pdf")
    print("Report generated successfully!")



#generate_report()

