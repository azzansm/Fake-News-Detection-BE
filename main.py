from fastapi import FastAPI, HTTPException
import logging
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utils.highlight import highlight_sentences
from utils.sentiment import analyze_sentiment
from utils.testing import get_predictions

# FastAPI setup
app = FastAPI()

# Enable CORS for React frontend (allowing localhost, local network IP, and deployed frontend URL)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",  # Localhost for development
        "http://localhost:80",  # Allow frontend running locally on port 80
        "http://192.168.1.3",
        "http://192.168.1.3:80", # Replace with your local network IP or use `*` for all IPs (less secure)
        "https://fake-news-detection-va.vercel.app",
        "http://192.168.56.1:80", 
        "http://192.168.56.1",
        "*",
        # Production frontend URL (if applicable)
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # Allow specific methods
    allow_headers=["*"],
)

# Define a request model for the predict endpoint
class PredictRequest(BaseModel):
    news_text: str

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.get("/")
async def root():
    return {"message": "Welcome to the Fake News Prediction API"}

@app.post("/predict", responses={
    200: {"description": "Prediction successful", "content": {"application/json": {}}},
    500: {"description": "Server error"}
})
async def predict(request: PredictRequest):
    try:
        # Highlight sentences in the news
        highlighted_text, color_meanings = highlight_sentences(request.news_text)
        logging.info(f"Highlighted text: {highlighted_text}")

        # Analyze sentiment of the news
        sentiment = analyze_sentiment(request.news_text)
        logging.info(f"Sentiment analysis result: {sentiment}")

        # Perform predictions using models
        predictions, confidences = get_predictions(request.news_text)  
        logging.info(f"Predictions: {predictions}, Confidences: {confidences}")

        # Find the model with the highest confidence
        max_confidence_model = max(confidences, key=confidences.get)
        max_confidence_prediction = predictions[max_confidence_model]
        max_confidence_value = confidences[max_confidence_model]

        # Prepare the response structure
        return {
            "confidences": confidences,
            "highlighted": highlighted_text,
            "sentiment": sentiment,
            "color_meanings": color_meanings,
            "predictions": predictions,
            "max_confidence_model": max_confidence_model,
            "max_confidence_prediction": max_confidence_prediction,
            "max_confidence_value": max_confidence_value,
        }

    except Exception as e:
        logging.error(f"Error during prediction: {e}")
        raise HTTPException(status_code=500, detail="Failed to process prediction request.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

