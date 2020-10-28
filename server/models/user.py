from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field

class UserSchema(BaseModel):
    firstName: str = Field(...)
    lastName: str = Field(...)
    email: EmailStr = Field(...)
    department: Optional[str] = None
    status: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "firstName": "John",
                "lastName": "Doe",
                "email": "j.doe@focal.com",
                "department": "IT",
                "status": "Working remotely"
            }
        }


class UpdateUserModel(BaseModel):
    firstName: Optional[str]
    lastName: Optional[str]
    email: Optional[EmailStr]
    department: Optional[str]
    status: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "firstName": "John",
                "lastName": "Doe",
                "email": "j.doe@focal.com",
                "department": "IT",
                "status": "Working remotely"
            }
        }


class UserResponseModel(BaseModel):
    responseMessage: str
    user: Optional[dict]
    # id: Optional[str]
    # firstName: Optional[str]
    # lastName: Optional[str]
    # email: Optional[EmailStr]
    # department: Optional[str]
    # status: Optional[str]


class UsersResponseModel(BaseModel):
    responseMessage: str
    users: Optional[List[dict]]
