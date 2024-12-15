from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer

# Initialize sentiment intensity analyzer
sia = SentimentIntensityAnalyzer()

# Function to analyze sentiment using TextBlob and VADER
def analyze_sentiment(text):
    # TextBlob Sentiment Analysis (polarity)
    blob = TextBlob(text)
    textblob_polarity = blob.sentiment.polarity  # Range from -1 (negative) to 1 (positive)
    
    # VADER Sentiment Analysis (positive, neutral, negative)
    vader_scores = sia.polarity_scores(text)
    vader_pos = vader_scores['pos']
    vader_neg = vader_scores['neg']
    vader_neu = vader_scores['neu']
    
    # Categorize sentiment as Positive, Negative, or Neutral based on polarity scores
    if textblob_polarity > 0:
        sentiment = "Positive"
    elif textblob_polarity < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    
    # Return sentiment results and scores
    return sentiment, textblob_polarity, vader_pos, vader_neg, vader_neu

# from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

# # Load the model and tokenizer
# model_name = "distilbert-base-uncased-finetuned-sst-2-english"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForSequenceClassification.from_pretrained(model_name)

# # Create the sentiment analysis pipeline with truncation enabled
# bert_sentiment_analyzer = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# def analyze_sentiment(text):
#     # Use the pipeline to get sentiment analysis with truncation
#     result = bert_sentiment_analyzer(text, truncation=True, padding=True)
    
#     sentiment_label = result[0]['label']
#     sentiment_score = result[0]['score']
    
#     return sentiment_label, sentiment_score
