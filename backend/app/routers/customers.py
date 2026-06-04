from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.customer_schema import CustomerCreate, CustomerRead
from app.services.customer_service import CustomerService

router = APIRouter()


@router.get("/", response_model=List[CustomerRead])
def list_customers(db: Session = Depends(get_db)):
    return CustomerService(db).get_all()


@router.post("/", response_model=CustomerRead)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    return CustomerService(db).create(customer)


@router.get("/{customer_id}", response_model=CustomerRead)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = CustomerService(db).get_by_id(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Không tìm thấy khách hàng")
    return customer
