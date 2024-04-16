"""
Parts:
1.registration and login service with fastapi. Authentication with jwt for secure/conversation endpoin
2. Integrate ChatBot with langchain and OpenAI
JWT: JSON Web token
"""


from pydantic import BaseModel
from typing import Optional
from enum import Enum


# this class has three properties or category for out fittness app
class UserLevel(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    expert = "expert"
    

class UserBase(BaseModel):
    email:str
    username:str
    age:Optional[int] = None
    level:UserLevel = UserLevel.beginner
    

# In the api user will pass passwrod as normal string but password is stored as 
# hash in the database
class UserIn(UserBase):
    password: str


# So for this we will create two class, the database version and for api  
class UserInDBBase(UserBase):
    id:int 

    # this will convert sqlalchemy to convert this to database class
    class Config: 
        orm_mode = True
    
    
class UserInDB(UserInDBBase): # this is the password class for database 
    hashed_password:str
    
class TokenData(BaseModel): # class related to token, inherited from basemodel.
    username: Optional[str] = None 
    # username is stored in the jwt 
    
# this is token
class Token(BaseModel):
    access_token :str
    token_type:str