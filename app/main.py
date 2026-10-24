from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

class Expense(BaseModel):
    amount: float
    category: str
    description: str




@app.get("/")
def root():
    return {"message": "Expense Tracker API is running"}


@app.post("/expenses")
def create_expense(expense: Expense):
    return expense
