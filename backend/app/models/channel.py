from sqlalchemy import Column, Integer, String

from app.database import Base


class Channel(Base):
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    provider = Column(String, nullable=True)
