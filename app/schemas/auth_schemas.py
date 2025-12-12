from pydantic import BaseModel, EmailStr

class AdminLogin(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    message: str
    token: str
    org_name: str