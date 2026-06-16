from pydantic import BaseModel


class AdminLogin(BaseModel):
    admin_id: str
    password: str
