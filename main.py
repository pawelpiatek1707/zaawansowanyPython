from typing import Union
import math
from fastapi import FastAPI, Query, HTTPException

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

