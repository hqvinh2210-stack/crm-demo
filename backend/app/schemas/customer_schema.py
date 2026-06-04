from pydantic import BaseModel, EmailStr


class CustomerBase(BaseModel):
    name: str
    email: EmailStr | None = None
    phone: str | None = None
    status: str | None = None
    notes: str | None = None


class CustomerCreate(CustomerBase):
    pass


class CustomerRead(CustomerBase):
    id: int

    model_config = {
        "from_attributes": True,
    }
