# import pickle
# import tensorflow as tf
# import os
# import nltk
# from nltk.corpus import stopwords

# # Ensure stopwords are downloaded
# nltk.download('stopwords')

# # Preprocessing function (commented out for testing without preprocessing)
# stop_words = set(stopwords.words('english'))

# def preprocess_text(text):
#     text = text.lower()  # Convert to lowercase
#     text = ''.join([char if char.isalnum() else ' ' for char in text])  # Remove special characters
#     text = ' '.join([word for word in text.split() if word not in stop_words])  # Remove stopwords
#     return text  # No preprocessing for testing

# # Ensure TensorFlow runs optimally
# os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# # Load tokenizers
# with open('models/tokenizer_gru_FINAL.pkl', 'rb') as handle:
#     gru_tokenizer = pickle.load(handle)

# with open('models/tokenizer_bidir_FINAL.pkl', 'rb') as handle:
#     bidir_tokenizer = pickle.load(handle)

# with open('models/tokenizer_lstm_FINAL.pkl', 'rb') as handle:
#     lstm_tokenizer = pickle.load(handle)

# with open('models/tokenizer_rnn_FINAL.pkl', 'rb') as handle:
#     rnn_tokenizer = pickle.load(handle)

# with open('models/tokenizer_coattention_FINAL.pkl', 'rb') as handle:
#     coattention_tokenizer = pickle.load(handle)

# # Prediction function
# def predict_with_model(model, tokenizer, input_text, model_name):
#     # Preprocess input
#     processed_text = preprocess_text(input_text)

#     # Tokenize and pad input
#     sequences = tokenizer.texts_to_sequences([processed_text])
#     maxlen = model.input_shape[1]
#     padded_sequences = tf.keras.preprocessing.sequence.pad_sequences(sequences, maxlen=maxlen, padding='post')

#     # Convert to tensor
#     input_tensor = tf.convert_to_tensor(padded_sequences, dtype=tf.float32)

#     # Get prediction
#     output = model(input_tensor)
    
#     # Debugging: print the raw output before applying sigmoid
#     print(f"Raw output for {model_name}: {output.numpy()}")

#     # Apply sigmoid to get the probability
#     # prediction = float(tf.sigmoid(output).numpy()[0][0])
#     raw_score = float(output.numpy()[0][0])
#     # return prediction
#     return raw_score

# def get_predictions(input_text):
#     models_info = [
#         {'path': 'models/gru_FINAL.h5', 'name': 'GRU', 'tokenizer': gru_tokenizer},
#         {'path': 'models/bidir_FINAL.h5', 'name': 'BiDir-LSTM-CNN', 'tokenizer': bidir_tokenizer},
#         {'path': 'models/lstm_FINAL.h5', 'name': 'LSTM', 'tokenizer': lstm_tokenizer},
#         {'path': 'models/rnn_FINAL.h5', 'name': 'RNN', 'tokenizer': rnn_tokenizer},
#         {'path': 'models/coattention_FINAL.h5', 'name': 'Coattention', 'tokenizer': coattention_tokenizer}
#     ]

#     models = {}
#     for model_info in models_info:
#         try:
#             model = tf.keras.models.load_model(model_info['path'])
#             models[model_info['name']] = (model, model_info['tokenizer'])
#         except Exception as e:
#             print(f"Error loading {model_info['name']}: {e}")

#     predictions = {}
#     confidences = {}

#     # Get predictions and their raw scores
#     for model_name, (model, tokenizer) in models.items():
#         raw_score = predict_with_model(model, tokenizer, input_text, model_name)
        
#         # Classify as "Real" if raw_score >= 0.5, else "Fake"
#         predictions[model_name] = "Real" if raw_score >= 0.5 else "Fake"
        
#         # Set confidence based on raw score
#         confidences[model_name] = raw_score if raw_score >= 0.5 else 1 - raw_score

#     return predictions, confidences

import pickle
import tensorflow as tf
import os
import nltk
from nltk.corpus import stopwords
import requests

# Ensure stopwords are downloaded
nltk.download('stopwords')

# Preprocessing function (commented out for testing without preprocessing)
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    text = text.lower()  # Convert to lowercase
    text = ''.join([char if char.isalnum() else ' ' for char in text])  # Remove special characters
    text = ' '.join([word for word in text.split() if word not in stop_words])  # Remove stopwords
    return text  # No preprocessing for testing

# Ensure TensorFlow runs optimally
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Load tokenizers
with open('models/tokenizer_gru_FINAL.pkl', 'rb') as handle:
    gru_tokenizer = pickle.load(handle)

with open('models/tokenizer_bidir_FINAL.pkl', 'rb') as handle:
    bidir_tokenizer = pickle.load(handle)

with open('models/tokenizer_lstm_FINAL.pkl', 'rb') as handle:
    lstm_tokenizer = pickle.load(handle)

with open('models/tokenizer_rnn_FINAL.pkl', 'rb') as handle:
    rnn_tokenizer = pickle.load(handle)

with open('models/tokenizer_coattention_FINAL.pkl', 'rb') as handle:
    coattention_tokenizer = pickle.load(handle)

# Function to download the .h5 file from Google Drive
def download_model_from_gdrive(file_id, destination_path):
    url = f'https://drive.google.com/uc?export=download&id={file_id}'
    response = requests.get(url)
    if response.status_code == 200:
        with open(destination_path, 'wb') as f:
            f.write(response.content)
        print(f'Model downloaded successfully to {destination_path}')
    else:
        print(f'Failed to download model. Status code: {response.status_code}')

# Replace these file IDs with the Google Drive IDs of your model files
gru_file_id = '18lyQCw1j3mHT_AIUihdFeRmvsdyY-u9W' 
bidir_file_id = '1oCsEJ-qM4gcp6rw6c_Ba-RxABr1l5zjr'
lstm_file_id = '1g6M6k0NZV0oLaoQv18gI-kIg3h6W3rfG'
rnn_file_id = '10n-UKAvadenFIgp6mP_9reOzcUTPzpQ6'
coattention_file_id = '1ptvlWduFp32iyr18D_O1lCMOvrm8He0i'

# Download the models
download_model_from_gdrive(gru_file_id, 'models/gru_FINAL.h5')
download_model_from_gdrive(bidir_file_id, 'models/bidir_FINAL.h5')
download_model_from_gdrive(lstm_file_id, 'models/lstm_FINAL.h5')
download_model_from_gdrive(rnn_file_id, 'models/rnn_FINAL.h5')
download_model_from_gdrive(coattention_file_id, 'models/coattention_FINAL.h5')

# Prediction function
def predict_with_model(model, tokenizer, input_text, model_name):
    # Preprocess input
    processed_text = preprocess_text(input_text)

    # Tokenize and pad input
    sequences = tokenizer.texts_to_sequences([processed_text])
    maxlen = model.input_shape[1]
    padded_sequences = tf.keras.preprocessing.sequence.pad_sequences(sequences, maxlen=maxlen, padding='post')

    # Convert to tensor
    input_tensor = tf.convert_to_tensor(padded_sequences, dtype=tf.float32)

    # Get prediction
    output = model(input_tensor)
    
    # Debugging: print the raw output before applying sigmoid
    print(f"Raw output for {model_name}: {output.numpy()}")

    # Apply sigmoid to get the probability
    raw_score = float(output.numpy()[0][0])
    return raw_score

def get_predictions(input_text):
    models_info = [
        {'path': 'models/gru_FINAL.h5', 'name': 'GRU', 'tokenizer': gru_tokenizer},
        {'path': 'models/bidir_FINAL.h5', 'name': 'BiDir-LSTM-CNN', 'tokenizer': bidir_tokenizer},
        {'path': 'models/lstm_FINAL.h5', 'name': 'LSTM', 'tokenizer': lstm_tokenizer},
        {'path': 'models/rnn_FINAL.h5', 'name': 'RNN', 'tokenizer': rnn_tokenizer},
        {'path': 'models/coattention_FINAL.h5', 'name': 'Coattention', 'tokenizer': coattention_tokenizer}
    ]

    models = {}
    for model_info in models_info:
        try:
            model = tf.keras.models.load_model(model_info['path'])
            models[model_info['name']] = (model, model_info['tokenizer'])
        except Exception as e:
            print(f"Error loading {model_info['name']}: {e}")

    predictions = {}
    confidences = {}

    # Get predictions and their raw scores
    for model_name, (model, tokenizer) in models.items():
        raw_score = predict_with_model(model, tokenizer, input_text, model_name)
        
        # Classify as "Real" if raw_score >= 0.5, else "Fake"
        predictions[model_name] = "Real" if raw_score >= 0.5 else "Fake"
        
        # Set confidence based on raw score
        confidences[model_name] = raw_score if raw_score >= 0.5 else 1 - raw_score

    return predictions, confidences
