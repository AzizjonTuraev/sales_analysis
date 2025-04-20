from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
# from . import server_utils
import server_utils
import json

# FastAPI app
app = FastAPI()

# Enable CORS (for frontend to communicate with API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model for POST request
class UserRequest(BaseModel):
    product_name: str
    forward_week_curve: int = 1


@app.get("/")
def home():
    return {"message": "Welcome to the Book Recommendation API"}


@app.post("/weekly_predictions")
def get_weekly_predictions(request: UserRequest):
    """
    Get a weekly forward demand prediction for a chosen product name. 
    Number of forward curves can be also specified. By default it predicts for the next 1 week
    """
    product_name = request.product_name
    forward_week_curve = request.forward_week_curve

    try:
        predictions = server_utils.get_prediction(product_name, forward_week_curve)
        return Response(
            content=json.dumps(predictions),
            media_type="application/json"
        ) # Convert dict to JSON
    except HTTPException as e:
        raise e  # Let FastAPI handle the exception and send the error response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
    
