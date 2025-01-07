import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle

# Load dataset
data = pd.read_csv('data/thought_categorization.csv')

# Preprocess and split data
X = data['thought']
y = data['category']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Convert text to numerical features using CountVectorizer
vectorizer = CountVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train Multinomial Naive Bayes model for CBT feature
model = MultinomialNB()
model.fit(X_train_vec, y_train)

# Evaluate the model
y_pred = model.predict(X_test_vec)
print(classification_report(y_test, y_pred))

# Save the model and vectorizer
with open('models/thought_classifier.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('models/thought_vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)


# Same thing. Once saved in a pickle file, will be reused again and again for test user data.