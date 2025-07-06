from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import date

class UserRegistration(BaseModel):
    name:str
    email:EmailStr
    password:str

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    id:int
    name:str
    email:EmailStr
    
class TaskCreate(BaseModel):
    title:str
    description:Optional[str]=None
    status:Optional[str]="Pending"
    due_date:Optional[date]=None
    user_id:int

class TaskResponse(BaseModel):
    id:int
    title:str
    description:Optional[str]
    status:str
    due_date:Optional[date]
    user_id:int