import pickle
import tensorflow as tf
import os
import nltk
from nltk.corpus import stopwords

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
    # prediction = float(tf.sigmoid(output).numpy()[0][0])
    raw_score = float(output.numpy()[0][0])
    # return prediction
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
