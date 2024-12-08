# Step 1: Import relevant libraries
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# Step 2: Initialize FastAPI app
app = FastAPI()


# Step 3: Define the structure of the incoming data
class Transaction(BaseModel):
    transaction_id: str
    amount: float
    timestamp: datetime


# Define a basic endpoint to check if the API is running
@app.get("/")
def read_root():
    return {"message": "API is running successfully!"}


# Open your browser and visit: http://127.0.0.1:8000
# Or check the auto_generated documenation: http://127.0.0.1:8000/docs


# Step 3: Create a POST endpoint to receive and validate transactions
@app.post("/transactions")
def add_transaction(transaction: Transaction):
    # Validate data (FastAPI + Pydantic automatically handles validation here)
    # Log the received data
    print(f"Received transaction: {transaction}")

    # Return a success message
    return {"message": "Transaction received successfully", "data": transaction}
