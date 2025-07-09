from typing import Annotated

from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token/test")

@router.get("/items/oauth2")
async def read_items_oauth2(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


### GETTING CURRENT USER ###

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
    
def fake_decode_token_example(token):
    """
    Simulates decoding a token and returning a user.
    In a real application, you would verify the token and extract user information.
    """
    return User(username=token + "fakedecoded", email="john@example.com", full_name="John Doe")

async def get_current_user_ex(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token_example(token)
    return user

@router.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user_ex)]):
    return current_user

### Simple OAuth2 with Password and Bearer ###

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException, status

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

def fake_hash_password(password: str):
    return "fakehashed" + password

class UserInDB(User):
    hashed_password: str
    
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    
def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next section
    user = get_user(fake_users_db, token)
    return user

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@router.post("/token/test")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    # This is where you would create a real token
    # For simplicity, we return the username as the token
    # This is not secure and should not be used in production
    return {"access_token": user.username, "token_type": "bearer"}

@router.get("/users/me/oauth2/test")
async def read_users_me_oauth2(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user