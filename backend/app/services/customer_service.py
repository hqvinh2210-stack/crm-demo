from sqlalchemy.orm import Session

from app import models
from app.schemas.customer_schema import CustomerCreate


class CustomerService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(models.Customer).all()

    def get_by_id(self, customer_id: int):
        return self.db.query(models.Customer).filter(models.Customer.id == customer_id).first()

    def create(self, customer: CustomerCreate):
        db_customer = models.Customer(**customer.model_dump())
        self.db.add(db_customer)
        self.db.commit()
        self.db.refresh(db_customer)
        return db_customer
