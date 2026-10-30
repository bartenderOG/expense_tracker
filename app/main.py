

from fastapi import Depends, FastAPI
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from app import models
from app.database import SessionLocal, engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


class ExpenseCreate(BaseModel):
    amount: float
    category: str
    description: str


class ExpenseResponse(BaseModel):
    id: int
    amount: float
    category: str
    description: str

    model_config = ConfigDict(from_attributes=True)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Expense Tracker API is running"}


@app.post("/expense", response_model=ExpenseResponse)
def create_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
):
    new_expense = models.Expense(
        amount=expense.amount,
        category=expense.category,
        description=expense.description,
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense

@app.get("/expenses", response_model=list[ExpenseResponse])
def get_expenses(db: Session = Depends(get_db)):
    expenses = db.query(models.Expense).all()
    return expenses