import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import pickle
import re

# Download NLTK resources 
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

# Initialize preprocessing tools
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Preprocessing function -  dedicated preprocessing fucntion for text
def preprocess_text(text):
    # Lowercase
    text = text.lower()
    # Remove punctuation and special characters
    text = re.sub(r'[^\w\s]', '', text)
    # Tokenization
    tokens = word_tokenize(text)
    # Lemmatization and removing stop words
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    return " ".join(tokens)

# Load dataset form local storage
df = pd.read_csv('data/sentiment140.csv', encoding='latin1', names=['target', 'id', 'date', 'flag', 'user', 'text'])
df['sentiment'] = df['target'].map({0: 'negative', 2: 'neutral', 4: 'positive'})
df = df[['text', 'sentiment']]

# Preprocess text that is ready for model training
df['cleaned_text'] = df['text'].apply(preprocess_text)

# Split data
X = df['cleaned_text']
y = df['sentiment']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Convert text to bag-of-words representation to vectorize text
from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer()
X_train_vectorized = vectorizer.fit_transform(X_train)
X_test_vectorized = vectorizer.transform(X_test)

# Train a Logistic Regression model
model = LogisticRegression(max_iter=500, solver='lbfgs')  # Increase iterations
model.fit(X_train_vectorized, y_train)

# Evaluate the model
y_pred = model.predict(X_test_vectorized)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Save model and vectorizer
with open('models/sentiment_model.pkl', 'wb') as f:
    pickle.dump(model, f)
with open('models/vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

# The model is saved. This module will not be run again and again as the model is once saved, is ready to be used on test data.