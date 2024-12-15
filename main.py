from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router import router  # Import the router you created

# FastAPI setup
app = FastAPI()

# Enable CORS for Vercel frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://fake-news-detection-va.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the router
app.include_router(router)

@app.get("/")
async def root():
    """Root endpoint for testing API connectivity."""
    return {"message": "Welcome to the Fake News Prediction API"}
