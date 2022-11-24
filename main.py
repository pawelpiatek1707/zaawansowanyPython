from fastapi import FastAPI
from dotenv import load_dotenv
from routers import prime, picture, time

load_dotenv()

app = FastAPI()
app.include_router(prime.router)
app.include_router(picture.router)
app.include_router(time.router)



