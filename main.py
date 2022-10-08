import math
from fastapi import FastAPI, Query, UploadFile, HTTPException, File
from fastapi.responses import StreamingResponse
from PIL import Image, ImageOps
from io import BytesIO

app = FastAPI()

MAX_VALUE = 9223372036854775807


# python -m uvicorn main:app --reload

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


@app.get("/")
def read_root():
    return {"Hello": "World"}


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