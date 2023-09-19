from typing import Union
from fastapi import FastAPI
# from app.routers import maketaccount
from routers import maketaccount
import json

app = FastAPI()


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

def config_router():
    app.include_router(maketaccount.router)

config_router()
