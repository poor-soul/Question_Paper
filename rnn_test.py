import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load the saved model
model = load_model('question_generation_model.h5')

# Load preprocessed data
data = pd.read_csv(r"C:\Users\harsha anand\Desktop\Miniproject\extracted_questions.csv")  # Assuming your data is in a CSV file

# Drop rows with missing values in the 'Question' column
data = data.dropna(subset=['Question'])

# Separate features (X) and target variable (Y)
X = data['Question']

# Map ordinal categories to numerical values
difficulty_mapping = {"easy": 0, "medium": 1, "hard": 2}
data['Difficulty'] = data['Difficulty'].map(difficulty_mapping)

# Identify rows with missing values in the 'Difficulty' column
missing_indices = data[data['Difficulty'].isnull()].index

# Tokenize the text data using the same tokenizer used during training
tokenizer = Tokenizer()
tokenizer.fit_on_texts(X)

# Convert text data to sequences
X_seq = tokenizer.texts_to_sequences(X)

# Pad sequences
max_length = 100  # Should be the same as used during training
X_pad = pad_sequences(X_seq, maxlen=max_length, padding='post')

# Make predictions for missing values
predictions = model.predict(X_pad[missing_indices])

# Convert predictions to labels
predicted_labels = [difficulty_mapping[np.argmax(pred)] for pred in predictions]

# Fill in missing values with predicted labels
data.loc[missing_indices, 'Difficulty'] = predicted_labels

# Save the updated DataFrame to a new CSV file
data.to_csv('updated_data.csv', index=False)
