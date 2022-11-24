import math
import datetime
import os
from fastapi import FastAPI, Query, UploadFile, HTTPException, File, Depends
from fastapi.responses import StreamingResponse
from fastapi.security import OAuth2PasswordBearer
from PIL import Image, ImageOps
from io import BytesIO
from dotenv import load_dotenv

# TODO
# 1. Podzielić na bardziej sensowne pliki
# 2. Przenieść token do evn

load_dotenv()

app = FastAPI()

MAX_VALUE = 9223372036854775807


# python -m uvicorn main:app --reload


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def auth_request(token: str = Depends(oauth2_scheme)) -> bool:
    print('token: ', token)
    authenticated = token == os.getenv('API_TOKEN')
    print(os.environ.get('API_TOKEN'))
    return authenticated


def is_prime(n: int):
    if n == 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if (n % i) == 0:
            return False
    return True


def return_prime_exception(message: str):
    raise HTTPException(
        status_code=404, detail=message
    )


@app.get("/prime/{number}")
def read_item(number: str = Query(max_length=3)):
    global query_number
    try:
        query_number = int(number)
        if query_number < 1 or query_number > MAX_VALUE:
            return_prime_exception(f"Wrong value. Numbers between 1 and {MAX_VALUE} are acceptable")
        return {"is_prime": is_prime(int(query_number))}
    except ValueError:
        return_prime_exception(f"Wrong number type. Only int type ia acceptable")


@app.post("/picture/invert")
def invert_image(img: UploadFile = File(...)):
    original_image = Image.open(img.file)
    original_image = ImageOps.invert(original_image)
    filtered_image = BytesIO()
    original_image.save(filtered_image, "JPEG")
    filtered_image.seek(0)
    return StreamingResponse(filtered_image, media_type = "image/jpeg")


@app.get("/time")
def return_time(authenticated: bool = Depends(auth_request)):
    if not authenticated:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated")
    now = datetime.datetime.now()
    return {"time": f"{now.hour}:{now.minute}"}