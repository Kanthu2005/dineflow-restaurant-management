<<<<<<< HEAD
from datetime import datetime
from pydantic import BaseModel, EmailStr


class CustomerModel(BaseModel):
    name: str
    phone: str
    email: EmailStr | None = None
    created_at: datetime
    updated_at: datetime
=======
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class CustomerBase(BaseModel):
    name: str
    phone: str
    email: Optional[EmailStr] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None

class Customer(CustomerBase):
    id: str
    created_at: datetime
>>>>>>> main
