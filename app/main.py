
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from sqlalchemy import asc, desc
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
@app.put("/expense/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: int,
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
):
    existing_expense = db.query(models.Expense).filter(
        models.Expense.id == expense_id
    ).first()

    if existing_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")

    existing_expense.amount = expense.amount
    existing_expense.category = expense.category
    existing_expense.description = expense.description

    db.commit()
    db.refresh(existing_expense)

    return existing_expense

@app.get("/expenses", response_model=list[ExpenseResponse])
def get_expenses(
    category: str | None = Query(default=None),
    min_amount: float | None = Query(default=None, gt=0),
    max_amount: float | None = Query(default=None, gt=0),
    sort: str | None = Query(default=None),
    limit: int = Query(default=10, gt=0, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    if min_amount is not None and max_amount is not None:
        if min_amount > max_amount:
            raise HTTPException(
                status_code=400,
                detail="min_amount cannot be greater than max_amount",
            )
    query = db.query(models.Expense)

    if category:
        query = query.filter(models.Expense.category == category)
    if min_amount is not None:
        query = query.filter(models.Expense.amount >= min_amount)
    if max_amount is not None:
        query = query.filter(models.Expense.amount <= max_amount)
    if sort == "asc":
        query = query.order_by(asc(models.Expense.amount))
    elif sort == "desc":
        query = query.order_by(desc(models.Expense.amount))

    query = query.offset(offset).limit(limit)

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