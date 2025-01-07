# Mental Health Analytics App

The **Mental Health Analytics App** is a Streamlit-based application designed to assist therapists in quickly understanding their patients' mental health. This tool bridges the gap between patients in rural areas and therapists in urban centers by providing insights into patient moods, recurring thought patterns, and categorized concerns.

---

## Features

### 1. **Write Your Mood**
- Allows users to share their thoughts and moods.
- **Basic Version**:
  - Performs sentiment analysis (Positive, Negative, Neutral).
- **Pro Version**:
  - Performs multi-emotion classification using a pre-trained DistilBERT model.
  - Visualizes emotion distribution over time.

### 2. **Cognitive Corrections**
- Classifies recurring thoughts into predefined categories such as:
  - **Family**, **Finance**, **Relationships**, **Abuse**, **Health**, **Employment**, **Education**.
- Tracks and visualizes recurring themes over time to highlight areas of concern.

### 3. **PDF Report Generation**
- Generates a consolidated PDF report for therapists, including:
  - Mood trends and emotion distribution.
  - Categorized thought patterns.
  - Infographics for quick analysis.

---

## Installation

### Prerequisites
- Python 3.8+
- Git
- Virtual Environment (optional but recommended)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/Mental-Health-Analytics.git
   cd Mental-Health-Analytics
   ```
2. Create Virtual Environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
2. Install Dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run app:
   ```bash
   streamlit run main.py
   ```

---
