import pymongo
import datetime

# MongoDB connection string (directly hardcoded)
MONGODB_URI = "mongodb+srv://fnAdmin:fnAdminPW@fakenewsdb.a6jvc.mongodb.net/?retryWrites=true&w=majority"

# Connect to MongoDB
client = pymongo.MongoClient(MONGODB_URI)

# Specify the database you want to use (MongoDB will create it if it doesn't exist)
db = client.get_database("fakenewsdb")  # Replace 'fakenewsdb' with your desired database name

# Define collections
predictions_collection = db["predictions"]
logs_collection = db["logs"]

# Function to store predictions in MongoDB
def store_prediction(model_name, prediction, news_text, confidence):
    prediction_data = {
        "model_name": model_name,
        "prediction": prediction,
        "news_text": news_text,
        "confidence": confidence,
        "timestamp": datetime.datetime.utcnow(),
    }
    predictions_collection.insert_one(prediction_data)

# Function to store logs (e.g., for debugging or user activity)
def store_log(message):
    log_data = {
        "message": message,
        "timestamp": datetime.datetime.utcnow(),
    }
    logs_collection.insert_one(log_data)
