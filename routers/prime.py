from fastapi import APIRouter
from fastapi import Query, HTTPException
from consts.prime_max_value import MAX_VALUE
from helpers.is_prime import is_prime

router = APIRouter()


def return_prime_exception(message: str):
    raise HTTPException(
        status_code=404, detail=message
    )


@router.get("/prime/{number}")
def read_item(number: str = Query(max_length=3)):
    global query_number
    try:
        query_number = int(number)
        if query_number < 1 or query_number > MAX_VALUE:
            return_prime_exception(f"Wrong value. Numbers between 1 and {MAX_VALUE} are acceptable")
        return {"is_prime": is_prime(int(query_number))}
    except ValueError:
        return_prime_exception(f"Wrong number type. Only int type ia acceptable")
