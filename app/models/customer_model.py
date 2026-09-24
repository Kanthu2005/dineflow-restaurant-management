from datetime import datetime
from pydantic import BaseModel, EmailStr


class CustomerModel(BaseModel):
    name: str
    phone: str
    email: EmailStr | None = None
    created_at: datetime
    updated_at: datetime
