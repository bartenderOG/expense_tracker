
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field, field_validator

from sqlalchemy.orm import Session

from app import models
from app.database import SessionLocal, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    models.Base.metadata.create_all(bind=engine)
    yield



app = FastAPI(lifespan=lifespan)



class ExpenseCreate(BaseModel):
    amount: float = Field(gt=0)
    category: str = Field(min_length=1)
    description: str = Field(min_length=1)

    @field_validator("category")
    @classmethod
    def validate_category(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Category cannot be empty")

        return value.strip()

    @field_validator("description")
    @classmethod
    def validate_description(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Description cannot be empty")

        return value.strip()


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
def get_expenses(
    category: str | None = Query(default=None),
    min_amount: float | None = Query(default=None, gt=0),
    max_amount: float | None = Query(default=None, gt=0),
    db: Session = Depends(get_db),
):
    query = db.query(models.Expense)

    if category:
        query = query.filter(models.Expense.category == category)
    if min_amount is not None:
        query = query.filter(models.Expense.amount >= min_amount)
    if max_amount is not None:
        query = query.filter(models.Expense.amount <= max_amount)

    return query.all()

@app.delete("/expense/{expense_id}")
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
):
    expense = db.query(models.Expense).filter(
        models.Expense.id == expense_id
    ).first()

    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")

    db.delete(expense)
    db.commit()

    return {"message": "Expense deleted"}