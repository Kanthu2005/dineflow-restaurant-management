from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class CustomerCreate(BaseModel):
<<<<<<< HEAD
    name: str = Field(min_lenght=2, max_lenght=100)
=======
    name: str = Field(min_length=2, max_length=100)
>>>>>>> main
    phone: str = Field(min_length=10, max_length=15)
    email: EmailStr | None = None

class CustomerUpdate(BaseModel):
<<<<<<< HEAD
    name: str | None = Field(defalut=None, min_length=2, max_length=100)
    phone: str |None = Field(default=None, min_length=10, max_length=15)
=======
    name: str | None = Field(default=None, min_length=2, max_length=100)
    phone: str | None = Field(default=None, min_length=10, max_length=15)
>>>>>>> main
    email: EmailStr | None = None

class CustomerResponse(BaseModel):
    id: str
    name: str
    phone: str
    email: EmailStr | None = None 
    created_at: datetime
    updated_at: datetime