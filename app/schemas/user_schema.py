from pydantic import BaseModel

class UserRegisterRequest(BaseModel):
    username: str
    password: str

# class UserLoginRequest(BaseModel):
#     username: str
#     password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class UserProfileRequest(BaseModel):
    username: str
    roles: list[str]
    permissions: list[str]