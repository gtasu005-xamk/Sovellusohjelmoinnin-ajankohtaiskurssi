from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from pydantic_core import PydanticCustomError


common_passwords = [
    "password", "12345678", "qwerty1234","salasana", "salasana1","admin1234",

]


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=64)
    display_name: str = Field(min_length=8)

    @field_validator("password", mode="after")
    @classmethod
    def check_password(cls, value: str) -> str:
        if value in common_passwords:
            raise ValueError("Salasana on liian yleinen")
        if not any(c.isupper() for c in value) or not any(c.isdigit() for c in value):
            raise ValueError("Salasanassa pitää olla vähintään yksi iso kirjain ja yksi numero")
        return value

class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    display_name: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=64)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
