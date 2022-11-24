import os
import datetime
from fastapi import APIRouter
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def auth_request(token: str = Depends(oauth2_scheme)) -> bool:
    print('token: ', token)
    authenticated = token == os.getenv('API_TOKEN')
    return authenticated


@router.get("/time")
def return_time(authenticated: bool = Depends(auth_request)):
    if not authenticated:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated")
    now = datetime.datetime.now()
    return {"time": f"{now.hour}:{now.minute}"}