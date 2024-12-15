from fastapi import APIRouter
from utils.highlight import highlight_sentences
from utils.sentiment import analyze_sentiment
from utils.testing import get_predictions
from pydantic import BaseModel
from fastapi import HTTPException
import logging

# Create the router instance
router = APIRouter()

# Define a request model for the predict endpoint
class PredictRequest(BaseModel):
    news_text: str

# Configure logging
logging.basicConfig(level=logging.INFO)

@router.post("/predict", responses={
    200: {"description": "Prediction successful", "content": {"application/json": {}}},
    500: {"description": "Server error"}
})
async def predict(request: PredictRequest):
    """Process prediction, including highlighting, sentiment, and model predictions."""
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
