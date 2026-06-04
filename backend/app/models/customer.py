from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, index=True, nullable=True)
    phone = Column(String, index=True, nullable=True)
    status = Column(String, index=True, nullable=False, default="New lead")
    notes = Column(String, nullable=True)

    conversations = relationship("Conversation", back_populates="customer")
